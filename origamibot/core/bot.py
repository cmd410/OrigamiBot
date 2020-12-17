import shlex
import logging

from typing import List, Optional, Union, IO, Callable
from collections import deque
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import current_thread, Event
from time import sleep

from .sthread import StoppableThread
from .teletypes import (
    Update,
    Message,
    ReplyMarkup,
    InlineKeyboardMarkup,
    UserProfilePhotos,
    ChatPermissions,
    Chat,
    ChatMember,
    BotCommand,
    WebhookInfo,
    InputMedia,
    Poll,
    User
    )

from .teletypes.inline_query_result import InlineQueryResult

from .commands import CommandContainer
from .callbacks import Callbacks
from .util import check_args

from .api_request import (
    get_updates,
    get_me,
    send_message,
    forward_message,
    send_photo,
    send_audio,
    send_document,
    send_video,
    send_animation,
    send_voice,
    send_video_note,
    send_location,
    edit_message_live_location,
    stop_message_live_location,
    send_venue,
    send_contact,
    send_poll,
    send_dice,
    send_chat_action,
    get_user_profile_photos,
    kick_chat_member,
    unban_chat_member,
    restrict_chat_member,
    promote_chat_member,
    set_chat_administrator_custom_title,
    set_chat_permissions,
    export_chat_invite_link,
    set_chat_photo,
    delete_chat_photo,
    set_chat_title,
    set_chat_description,
    pin_chat_message,
    unpin_chat_message,
    leave_chat,
    get_chat,
    get_chat_administrators,
    get_chat_members_count,
    get_chat_member,
    set_chat_sticker_set,
    delete_chat_sticker_set,
    answer_callback_query,
    set_my_commands,
    get_my_commands,
    answer_inline_query,
    set_webhook,
    delete_webhook,
    get_webhook_info,
    edit_message_text,
    edit_message_caption,
    edit_message_media,
    edit_message_reply_markup,
    stop_poll,
    delete_message,
    send_media_group)

from ..listener import Listener


using_greenlets = False
try:
    import gevent
    from gevent.monkey import is_module_patched
    if any([
            is_module_patched('socket'),
            is_module_patched('threading'),
            is_module_patched('time')
            ]):
        using_greenlets = True
    else:
        del gevent
except ImportError:
    pass


logger = logging.getLogger('origamibot')


class OrigamiBot:
    """Telegram bot class."""
    def __init__(self, token):
        self.token = token
        self.webhook = None
        self.updates = deque()
        self.inline = deque()
        self.callback = deque()
        
        self.interval = 10
        self.update_limit = 100
        self.allowed_updates = []
        self.safe_poll = True

        self._name = None
        self.first_only_command = True

        self._listen_thread = StoppableThread(
            name='Listen thread',
            target=self._listen_loop,
            daemon=True)

        self._webhook_thread = StoppableThread(
            name='Webhook thread',
            target=self._webhook_loop,
            daemon=True)

        self._process_thread = StoppableThread(
            name='Update process thread',
            target=self._process_updates_loop,
            daemon=True)

        self._inline_thread = StoppableThread(
            name='Inline thread',
            target=self._inline_loop,
            daemon=True)

        self._callback_thread = StoppableThread(
            name='Inline thread',
            target=self._callback_loop,
            daemon=True)

        self.has_updates = Event()
        self.has_inline = Event()
        self.has_callback = Event()

        self._last_update_id = 0

        self.command_container = CommandContainer()
        self.inline_container = Callbacks()
        self.callback_container = Callbacks()
        self.listeners = []

    @property
    def name(self):
        if self._name is None:
            self._name = self.get_me().username
        return self._name

    @property
    def is_alive(self):
        return all(
            [
                self._listen_thread.is_alive(),
                self._process_thread.is_alive(),
                self._callback_thread.is_alive(),
                self._inline_thread.is_alive()
            ]
        )

    def start(self,
              webhook=False,
              poll=True, 
              process=True,
              inline=True,
              callback=True):
        """Start listening for updates. Non-blocking!
        
        start_webhook=False - Start inbuilt webhook server
        poll=True - Start Polling thread
        process=True - Start update processing thread
        inline=True - Start separate inline thread
        """
        if webhook and not poll:
            self._webhook_thread.start()
        elif poll:
            self._listen_thread.start()
        if process:
            self._process_thread.start()
        if inline:
            self._inline_thread.start()
        if callback:
            self._callback_thread.start()

    def stop(self):
        """Terminate all bot's threads."""
        if self._listen_thread.is_alive():
            self._listen_thread.stop()
            self._listen_thread.join()
        if self._process_thread.is_alive():
            self._process_thread.stop()
            self._process_thread.join()
        if self._inline_thread.is_alive():
            self._inline_thread.stop()
            self._inline_thread.join()

    def process_update(self, update: Update):
        """Process a single update."""
        if update.message is not None:
            update.message.bot = self
            self._call_listeners(
                'on_message',
                update.message)
            self._handle_message(update.message)
        elif update.channel_post is not None:
            self._call_listeners(
                'on_channel_post',
                update.channel_post)
        elif update.edited_message is not None:
            self._call_listeners(
                'on_edited_message',
                update.edited_message)
        elif update.edited_channel_post is not None:
            self._call_listeners(
                'on_edited_channel_post',
                update.edited_channel_post)
        elif update.inline_query is not None:
            if self._inline_thread.is_alive():
                self.inline.append(update.inline_query)
                self.has_inline.set()
            else:
                self.inline_container.call(update.inline_query)
        elif update.callback_query is not None:
            if self._callback_thread.is_alive():
                self.callback.append(update.callback_query)
                self.has_callback.set()
            else:
                self.callback_container.call(update.callback_query)

    def add_commands(self, obj):
        """Add an object to bot's commands container.

        Object's methods, not preceded with underscore
        will be considered bot's commands.
        """
        self.command_container.add_command(obj)

    def remove_commands(self, obj):
        self.command_container.remove(obj)

    def add_listener(self, obj):
        if not isinstance(obj, Listener):
            raise TypeError(f'{obj} is not a Listener')
        self.listeners.append(obj)

    def add_inline(self, obj):
        self.inline_container.add(obj)

    def remove_inline(self, obj):
        self.inline_container.remove(obj)

    def add_callback(self, obj):
        self.callback_container.add(obj)

    def remove_callback(self, obj):
        self.callback_container.remove(obj)

    def remove_commands_by_filter(self, filter_func: Callable):
        """Remove commands from container by filter

        Filter must be a callable with single argument(item)
        and should return True for each item that needs removing
        """
        self.command_container.remove_by_filter(filter_func)

    def clear_commands(self):
        """Remove all commands"""
        self.command_container.clear()

    def get_updates(self,
                    limit: int = -1,
                    timeout: int = -1,
                    allowed_updates: list = None
                    ) -> List[Update]:
        """Make getUpdate request to telegram API. Return list of updates"""
        if timeout == -1:
            timeout = self.interval

        if limit == -1:
            limit = self.update_limit

        if allowed_updates is None:
            allowed_updates = self.allowed_updates

        updates = get_updates(
            self.token,
            self._last_update_id,
            limit=limit,
            timeout=timeout,
            allowed_updates=allowed_updates
        )

        if updates:
            self._last_update_id = updates[-1].update_id

        return updates

    def get_me(self) -> User:
        return get_me(self.token)

    def send_message(self,
                     chat_id: Union[int, str],
                     text: str,
                     parse_mode: Optional[str] = None,
                     disable_web_page_preview: Optional[bool] = None,
                     disable_notification: Optional[bool] = None,
                     reply_to_message_id: Optional[int] = None,
                     reply_markup: Optional[ReplyMarkup] = None) -> Message:
        """Use this method to send text messages.

        On success, the sent Message is returned.
        """
        return send_message(self.token,
                            chat_id,
                            text,
                            parse_mode,
                            disable_web_page_preview,
                            disable_notification,
                            reply_to_message_id,
                            reply_markup)

    def reply_to(self, 
                 msg: Message,
                 text: str, 
                 parse_mode: Optional[str] = None,
                 disable_web_page_preview: Optional[bool] = None,
                 disable_notification: Optional[bool] = None,
                 reply_markup: Optional[ReplyMarkup] = None) -> Message:
        mid = msg.message_id
        cid = msg.chat.id
        return self.send_message(
            cid,
            text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=mid,
            reply_markup=reply_markup
        )

    def forward_message(self,
                        chat_id: Union[int, str],
                        from_chat_id: Union[int, str],
                        message_id: int,
                        disable_notification: Optional[bool] = None
                        ) -> Message:
        """Use this method to forward messages of any kind.

        On success, the sent Message is returned."""
        return forward_message(
            self.token,
            chat_id,
            from_chat_id,
            message_id,
            disable_notification
        )

    def send_photo(self,
                   chat_id: Union[int, str],
                   photo: Union[str, IO],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None) -> Message:
        """Use this method to send photos.

        On success, the sent Message is returned.
        """
        return send_photo(
            self.token,
            chat_id,
            photo,
            caption,
            parse_mode,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_audio(self,
                   chat_id: Union[int, str],
                   audio: Union[str, IO],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   duration: Optional[int] = None,
                   performer: Optional[str] = None,
                   title: Optional[str] = None,
                   thumb: Optional[Union[str, IO]] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None
                   ) -> Message:
        """Use this method to send audio files.

        Your audio must be in the .MP3 or .M4A format.
        On success, the sent Message is returned.
        """
        return send_audio(
            self.token,
            chat_id,
            audio,
            caption,
            parse_mode,
            duration,
            performer,
            title,
            thumb,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_document(self,
                      chat_id: Union[int, str],
                      document: Union[str, IO],
                      thumb: Optional[Union[str, IO]] = None,
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      disable_notification: Optional[bool] = None,
                      reply_to_message_id: Optional[int] = None,
                      reply_markup: Optional[ReplyMarkup] = None
                      ) -> Message:
        """Use this method to send general files.

        On success, the sent Message is returned.
        """
        return send_document(
            self.token,
            chat_id,
            document,
            thumb,
            caption,
            parse_mode,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_video(self,
                   chat_id: Union[int, str],
                   video: Union[str, IO],
                   duration: Optional[int] = None,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   thumb: Optional[Union[str, IO]] = None,
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   supports_streaming: Optional[bool] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None
                   ) -> Message:
        """Use this method to send video files.

        Telegram clients support mp4 videos
        (other formats may be sent as Document).
        On success, the sent Message is returned.
        """
        return send_video(
            self.token,
            chat_id,
            video,
            duration,
            width,
            height,
            thumb,
            caption,
            parse_mode,
            supports_streaming,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_animation(self,
                       chat_id: Union[int, str],
                       animation: Union[str, IO],
                       duration: Optional[int] = None,
                       width: Optional[int] = None,
                       height: Optional[int] = None,
                       thumb: Optional[Union[str, IO]] = None,
                       caption: Optional[Union[str, IO]] = None,
                       parse_mode: Optional[str] = None,
                       disable_notification: Optional[bool] = None,
                       reply_to_message_id: Optional[int] = None,
                       reply_markup: Optional[ReplyMarkup] = None
                       ) -> Message:
        """Use this method to send animation files (GIF or video without sound).

        On success, the sent Message is returned.
        """
        return send_animation(
            self.token,
            chat_id,
            animation,
            duration,
            width,
            height,
            thumb,
            caption,
            parse_mode,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_voice(self,
                   chat_id: Union[int, str],
                   voice: Union[str, IO],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   duration: Optional[int] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None
                   ) -> Message:
        """Use this method to send audio files to display the file as a voice message.

        For this to work, your audio must be in an .OGG file encoded with OPUS.
        On success, the sent Message is returned.
        """
        return send_voice(
            self.token,
            chat_id,
            voice,
            caption,
            parse_mode,
            duration,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_video_note(self,
                        chat_id: Union[int, str],
                        video_note: Union[str, IO],
                        duration: Optional[int] = None,
                        length: Optional[int] = None,
                        thumb: Optional[Union[str, IO]] = None,
                        disable_notification: Optional[bool] = None,
                        reply_to_message_id: Optional[int] = None,
                        reply_markup: Optional[ReplyMarkup] = None
                        ) -> Message:
        """Use this method to send rounded square mp4 videos of up to 1 minute long.

        On success, the sent Message is returned."""
        return send_video_note(
            self.token,
            chat_id,
            video_note,
            duration,
            length,
            thumb,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_location(self,
                      chat_id: Union[int, str],
                      latitude: float,
                      longitude: float,
                      live_period: Optional[int] = None,
                      disable_notification: Optional[bool] = None,
                      reply_to_message_id: Optional[int] = None,
                      reply_markup: Optional[ReplyMarkup] = None
                      ) -> Message:
        """Use this method to send point on the map.

        On success, the sent Message is returned.
        """
        return send_location(
            self.token,
            chat_id,
            latitude,
            longitude,
            live_period,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def edit_message_live_location(self,
                                   latitude: float,
                                   longitude: float,
                                   chat_id: Optional[Union[int, str]] = None,
                                   message_id: Optional[int] = None,
                                   inline_message_id: Optional[str] = None,
                                   reply_markup:
                                   Optional[InlineKeyboardMarkup] = None
                                   ) -> Union[Message, bool]:
        """Use this method to edit live location messages.

        A location can be edited until its live_period expires
        or editing is explicitly disabled by a call to stopMessageLiveLocation.

        On success, if the edited message was sent by the bot,
        the edited Message is returned, otherwise True is returned.
        """
        return edit_message_live_location(
            self.token,
            latitude,
            longitude,
            chat_id,
            message_id,
            inline_message_id,
            reply_markup
        )

    def stop_message_live_location(self,
                                   chat_id:
                                   Optional[Union[int, str]] = None,
                                   message_id:
                                   Optional[int] = None,
                                   inline_message_id:
                                   Optional[str] = None,
                                   reply_markup:
                                   Optional[ReplyMarkup] = None,
                                   ) -> Union[Message, bool]:
        """Use this method to stop updating a live location message.

        On success, if the message was sent by the bot,
        the sent Message is returned,
        otherwise True is returned
        """

        return stop_message_live_location(
            self.token,
            chat_id,
            message_id,
            inline_message_id,
            reply_markup
        )

    def send_venue(self,
                   chat_id: Union[int, str],
                   latitude: float,
                   longitude: float,
                   title: str,
                   address: str,
                   foursquare_id: Optional[str] = None,
                   foursquare_type: Optional[str] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None
                   ) -> Message:
        """Use this method to send information about a venue.

        On success, the sent Message is returned.
        """
        return send_venue(
            self.token,
            chat_id,
            latitude,
            longitude,
            title,
            address,
            foursquare_id,
            foursquare_type,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_contact(self,
                     chat_id: Union[int, str],
                     phone_number: str,
                     first_name: str,
                     last_name: Optional[str] = None,
                     vcard: Optional[str] = None,
                     disable_notification: Optional[bool] = None,
                     reply_to_message_id: Optional[int] = None,
                     reply_markup: Optional[ReplyMarkup] = None
                     ) -> Message:
        """Use this method to send phone contacts.

        On success, the sent Message is returned.
        """
        return send_contact(
            self.token,
            chat_id,
            phone_number,
            first_name,
            last_name,
            vcard,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_poll(self,
                  chat_id: Union[int, str],
                  question: str,
                  options: List[str],
                  is_anonymous: Optional[bool] = None,
                  type: Optional[str] = None,
                  allows_multiple_answers: Optional[bool] = None,
                  correct_option_id: Optional[int] = None,
                  explanation: Optional[str] = None,
                  explanation_parse_mode: Optional[str] = None,
                  open_period: Optional[int] = None,
                  close_date: Optional[int] = None,
                  is_closed: Optional[bool] = None,
                  disable_notification: Optional[bool] = None,
                  reply_to_message_id: Optional[int] = None,
                  reply_markup: Optional[ReplyMarkup] = None
                  ) -> Message:
        """Use this method to send a native poll.

        On success, the sent Message is returned.
        """
        return send_poll(
            self.token,
            chat_id,
            question,
            options,
            is_anonymous,
            type,
            allows_multiple_answers,
            correct_option_id,
            explanation,
            explanation_parse_mode,
            open_period,
            close_date,
            is_closed,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_dice(self,
                  chat_id: Union[int, str],
                  emoji: Optional[str] = None,
                  disable_notification: Optional[bool] = None,
                  reply_to_message_id: Optional[int] = None,
                  reply_markup: Optional[ReplyMarkup] = None
                  ) -> Message:
        """Use this method to send an animated emoji that will display a random value.

        On success, the sent Message is returned.
        """
        return send_dice(
            self.token,
            chat_id,
            emoji,
            disable_notification,
            reply_to_message_id,
            reply_markup
        )

    def send_chat_action(self,
                         chat_id: Union[int, str],
                         action: str
                         ) -> bool:
        """Use this method to tell that something is happening on the bot's side.

        The status is set for 5 seconds or less,
        when a message arrives from your bot, clients clear its typing status

        Returns True on success.
        """
        return send_chat_action(
            self.token,
            chat_id,
            action
        )

    def send_media_group(self,
                         chat_id: Union[int, str],
                         media: List[InputMedia],
                         disable_notification: Optional[bool] = None,
                         reply_to_message_id: Optional[bool] = None
                         ) -> Message:
        """Use this method to send a group of photos or videos as an album.
        On success, an array of the sent Messages is returned
        """
        return send_media_group(
            self.token,
            chat_id,
            media,
            disable_notification,
            reply_to_message_id
        )

    def get_user_profile_photos(self,
                                user_id: int,
                                offset: Optional[int] = None,
                                limit: Optional[int] = None
                                ) -> UserProfilePhotos:
        """Use this method to get a list of profile pictures for a user.

        Returns a UserProfilePhotos object.
        """
        return get_user_profile_photos(
            self.token,
            user_id,
            offset,
            limit
        )

    def kick_chat_member(self,
                         chat_id: Union[int, str],
                         user_id: int,
                         until_date: Optional[int] = None
                         ) -> bool:
        """Use this method to kick a user from a group, a supergroup or a channel.

        The bot must be an administrator in the chat for this to work
        and must have the appropriate admin rights.

        Returns True on success.
        """
        return kick_chat_member(
            self.token,
            chat_id,
            user_id,
            until_date
        )

    def unban_chat_member(self,
                          chat_id: Union[int, str],
                          user_id: int
                          ) -> bool:
        """Use this method to unban
        a previously kicked user in a supergroup or channel.

        Returns True on success.
        """
        return unban_chat_member(
            self.token,
            chat_id,
            user_id
        )

    def restrict_chat_member(self,
                             chat_id: Union[int, str],
                             user_id: int,
                             permissions: ChatPermissions,
                             until_date: Optional[int] = None
                             ) -> bool:
        """Use this method to restrict a user in a supergroup.

        The bot must be an administrator in the supergroup
        for this to work and must have the appropriate admin rights.

        Pass True for all permissions to lift restrictions from a user.

        Returns True on success.
        """
        return restrict_chat_member(
            self.token,
            chat_id,
            user_id,
            permissions,
            until_date
        )

    def promote_chat_member(self,
                            chat_id: Union[int, str],
                            user_id: int,
                            can_change_info: Optional[bool] = None,
                            can_post_messages: Optional[bool] = None,
                            can_edit_messages: Optional[bool] = None,
                            can_delete_messages: Optional[bool] = None,
                            can_invite_users: Optional[bool] = None,
                            can_restrict_members: Optional[bool] = None,
                            can_pin_messages: Optional[bool] = None,
                            can_promote_members: Optional[bool] = None
                            ) -> bool:
        """Use this method to promote
        or demote a user in a supergroup or a channel.

        Returns True on success.
        """
        return promote_chat_member(
            self.token,
            chat_id,
            user_id,
            can_change_info,
            can_post_messages,
            can_edit_messages,
            can_delete_messages,
            can_invite_users,
            can_restrict_members,
            can_pin_messages,
            can_promote_members
        )

    def set_chat_administrator_custom_title(self,
                                            chat_id: Union[int, str],
                                            user_id: int,
                                            custom_title: int
                                            ) -> bool:
        """Use this method to set a custom title for an administrator
        in a supergroup promoted by the bot.

        Returns True on success."""

        return set_chat_administrator_custom_title(
            self.token,
            chat_id,
            user_id,
            custom_title
        )

    def set_chat_permissions(self,
                             chat_id: Union[int, str],
                             permissions: ChatPermissions
                             ) -> bool:
        """Use this method to set default chat permissions for all members.

        The bot must be an administrator in the group or a supergroup
        for this to work and must have the can_restrict_members admin rights.

        Returns True on success.
        """
        return set_chat_permissions(
            self.token,
            chat_id,
            permissions
        )

    def export_chat_invite_link(self,
                                chat_id: Union[int, str]
                                ) -> str:
        """Use this method to generate a new invite link for a chat;
        any previously generated link is revoked.

        Returns the new invite link as String on success.
        """
        return export_chat_invite_link(
            self.token,
            chat_id
        )

    def set_chat_photo(self,
                       chat_id: Union[int, str],
                       photo: IO
                       ) -> bool:
        """Use this method to set a new profile photo for the chat.

        Returns True on success.
        """
        return set_chat_photo(
            self.token,
            chat_id,
            photo
        )

    def delete_chat_photo(self,
                          chat_id: Union[int, str]
                          ) -> bool:
        """Use this method to delete a chat photo.

        Returns True on success.
        """
        return delete_chat_photo(
            self.token,
            chat_id
        )

    def set_chat_title(self,
                       chat_id: Union[int, str],
                       title: str
                       ) -> bool:
        """Use this method to change the title of a chat.

        Returns True on success.
        """
        return set_chat_title(
            self.token,
            chat_id,
            title
        )

    def set_chat_description(self,
                             chat_id: Union[int, str],
                             description: Optional[str] = None
                             ) -> bool:
        """Use this method to change the description of a group,
        a supergroup or a channel.

        Returns True on success.
        """
        return set_chat_description(
            self.token,
            chat_id,
            description
        )

    def pin_chat_message(self,
                         chat_id: Union[int, str],
                         message_id: int,
                         disable_notification: Optional[bool] = None
                         ) -> bool:
        """Use this method to pin a message in a group, a supergroup, or a channel.

        Returns True on success.
        """
        return pin_chat_message(
            self.token,
            chat_id,
            message_id,
            disable_notification
        )

    def unpin_chat_message(self,
                           chat_id: Union[int, str]
                           ) -> bool:
        """Use this method to unpin a message in a group, a supergroup, or a channel.

        Returns True on success.
        """
        return unpin_chat_message(
            self.token,
            chat_id
        )

    def leave_chat(self,
                   chat_id: Union[int, str]
                   ) -> bool:
        """Use this method for your bot to leave a group, supergroup or channel.

        Returns True on success.
        """
        return leave_chat(
            self.token,
            chat_id
        )

    def get_chat(self,
                 chat_id: Union[int, str]
                 ) -> Chat:
        """Use this method to get up to date information about the chat.

        Returns a Chat object on success.
        """
        return get_chat(
            self.token,
            chat_id
        )

    def get_chat_administrators(self,
                                chat_id: Union[int, str],
                                ) -> List[ChatMember]:
        """Use this method to get a list of administrators in a chat.

        On success, returns an Array of ChatMember objects
        that contains information about all chat administrators
        except other bots.
        """
        return get_chat_administrators(
            self.token,
            chat_id
        )

    def get_chat_members_count(self,
                               chat_id: Union[int, str]
                               ) -> int:
        """Use this method to get the number of members in a chat.

        Returns Int on success.
        """
        return get_chat_members_count(
            self.token,
            chat_id
        )

    def get_chat_member(self,
                        chat_id: Union[int, str],
                        user_id: int
                        ) -> ChatMember:
        """Use this method to get information about a member of a chat.

        Returns a ChatMember object on success.
        """
        return get_chat_member(
            self.token,
            chat_id,
            user_id
        )

    def set_chat_sticker_set(self,
                             chat_id: Union[int, str],
                             sticker_set_name: str
                             ) -> bool:
        """Use this method to set a new group sticker set for a supergroup

        Returns True on success.
        """
        return set_chat_sticker_set(
            self.token,
            chat_id,
            sticker_set_name
        )

    def delete_chat_sticker_set(self,
                                chat_id:  Union[int, str]
                                ) -> bool:
        """Use this method to delete a group sticker set from a supergroup.

        Returns True on success.
        """
        return delete_chat_sticker_set(
            self.token,
            chat_id
        )

    def answer_callback_query(self,
                              callback_query_id: str,
                              text: Optional[str] = None,
                              show_alert: Optional[bool] = None,
                              url: Optional[str] = None,
                              cache_time: Optional[int] = None
                              ) -> bool:
        """Use this method to send answers to callback queries
        sent from inline keyboards

        On success, True is returned.
        """
        return answer_callback_query(
            self.token,
            callback_query_id,
            text,
            show_alert,
            url,
            cache_time
        )

    def set_my_commands(self,
                        commands: List[BotCommand]
                        ) -> bool:
        """Use this method to change the list of the bot's commands.

        Returns True on success.
        """
        return set_my_commands(
            self.token,
            commands
        )

    def get_my_commands(self) -> List[BotCommand]:
        """Use this method to get the current list of the bot's commands.

        Returns Array of BotCommand on success.
        """
        return get_my_commands(self.token)

    def answer_inline_query(self,
                            inline_query_id: str,
                            results: List[InlineQueryResult],
                            cache_time: Optional[int] = None,
                            is_personal: Optional[bool] = None,
                            next_offset: Optional[str] = None,
                            switch_pm_text: Optional[str] = None,
                            switch_pm_parameter: Optional[str] = None
                            ) -> bool:
        """Use this method to send answers to an inline query.

        On success, True is returned.
        """
        return answer_inline_query(
            self.token,
            inline_query_id,
            results,
            cache_time,
            is_personal,
            next_offset,
            switch_pm_text,
            switch_pm_parameter
        )

    def set_webhook(self,
                    url: str,
                    certificate: Optional[IO] = None,
                    max_connections: Optional[int] = None,
                    allowed_updates: Optional[List[str]] = None
                    ) -> bool:
        """Use this method to specify a url
        and receive incoming updates via an outgoing webhook.

        Whenever there is an update for the bot,
        we will send an HTTPS POST request to the specified url,
        containing a JSON-serialized Update.

        Returns True on success.
        """
        self.webhook = url
        return set_webhook(
            self.token,
            url,
            certificate,
            max_connections,
            allowed_updates
        )

    def delete_webhook(self):
        """Use this method to remove webhook integration
        if you decide to switch back to getUpdates.

        Returns True on success.
        """
        return delete_webhook(self.token)

    def get_webhook_info(self) -> WebhookInfo:
        """Use this method to get current webhook status.

        On success, returns a WebhookInfo object.
        If the bot is using getUpdates,
        will return an object with the url field empty.
        """
        return get_webhook_info(self.token)

    def edit_message_text(self,
                          chat_id: Union[int, str],
                          text: str,
                          message_id: Optional[int] = None,
                          inline_message_id: Optional[str] = None,
                          parse_mode: Optional[str] = None,
                          disable_web_page_preview: Optional[bool] = None,
                          reply_markup: Optional[InlineKeyboardMarkup] = None
                          ) -> Union[Message, bool]:
        """Use this method to edit text and game messages.

        On success, if edited message is sent by the bot,
        the edited Message is returned,
        otherwise True is returned.
        """
        return edit_message_text(
            self.token,
            chat_id,
            text,
            message_id,
            inline_message_id,
            parse_mode,
            disable_web_page_preview,
            reply_markup
        )

    def edit_message_caption(self,
                             chat_id: Union[int, str],
                             caption: Optional[str] = None,
                             message_id: Optional[int] = None,
                             inline_message_id: Optional[str] = None,
                             parse_mode: Optional[str] = None,
                             reply_markup: Optional[
                                 InlineKeyboardMarkup] = None
                             ) -> Union[Message, bool]:
        """Use this method to edit captions of messages.

        On success, if edited message is sent by the bot,
        the edited Message is returned,
        otherwise True is returned.
        """
        return edit_message_caption(
            self.token,
            chat_id,
            caption,
            message_id,
            inline_message_id,
            parse_mode,
            reply_markup
        )

    def edit_message_media(self,
                           chat_id: Union[int, str],
                           media: InputMedia,
                           message_id: Optional[int] = None,
                           inline_message_id: Optional[int] = None,
                           reply_markup: Optional[InlineKeyboardMarkup] = None
                           ) -> Union[Message, bool]:
        """Use this method to edit animation, audio,
        document, photo, or video messages.

        On success, if the edited message was sent by the bot,
        the edited Message is returned,
        otherwise True is returned.
        """
        return edit_message_media(
            self.token,
            chat_id,
            media,
            message_id,
            inline_message_id,
            reply_markup
        )

    def edit_message_reply_markup(self,
                                  chat_id: Optional[Union[int, str]] = None,
                                  message_id: Optional[int] = None,
                                  inline_message_id: Optional[str] = None,
                                  reply_markup: Optional[
                                      InlineKeyboardMarkup] = None
                                  ) -> Union[Message, bool]:
        """Use this method to edit only the reply markup of messages.

        On success, if edited message is sent by the bot,
        the edited Message is returned,
        otherwise True is returned.
        """
        return edit_message_reply_markup(
            self.token,
            chat_id,
            message_id,
            inline_message_id,
            reply_markup
        )

    def stop_poll(self,
                  chat_id: Union[int, str],
                  message_id: int,
                  reply_markup: Optional[InlineKeyboardMarkup] = None
                  ) -> Poll:
        """Use this method to stop a poll which was sent by the bot.

        On success, the stopped Poll with the final results is returned.
        """
        return stop_poll(
            self.token,
            chat_id,
            message_id,
            reply_markup
        )

    def delete_message(self,
                       chat_id: Union[int, str],
                       message_id: int
                       ) -> bool:
        """Use this method to delete a message, including service messages

        Returns True on success.
        """
        return delete_message(
            self.token,
            chat_id,
            message_id
        )

    def _process_updates_loop(self):
        """The main processing thread.

        Is notified when updates arrive from listening thread
        and processes them one by one.
        """
        while True:
            self.has_updates.wait()
            while self.updates:
                self.process_update(self.updates.popleft())
            self.has_updates.clear()

    def _listen_loop(self):
        """Loop that repeatedly checks for updates.

        In main thread does nothing. And does not need to.
        """
        while True:
            if current_thread().stopped:
                break

            if self.safe_poll:
                try:
                    updates = self.get_updates()
                except (IOError, ConnectionError) as err:
                    logger.exception('Exception while polling')
                    self._call_listeners('on_poll_error', err)
                    sleep(2)
                    continue
            else:
                updates = self.get_updates()

            if updates:
                self.updates.extend(updates)
                self.has_updates.set()

    def _inline_loop(self):
        while True:
            if current_thread().stopped:
                break
            self.has_inline.wait()
            while self.inline:
                query = self.inline.popleft()
                if not using_greenlets:
                    self.inline_container.call(query)
                else:
                    gevent.spawn(self.inline_container.call, query)
            self.has_inline.clear()

    def _callback_loop(self):
        while True:
            if current_thread().stopped:
                break
            self.has_callback.wait()
            while self.callback:
                query = self.callback.popleft()
                if not using_greenlets:
                    self.callback_container.call(query)
                else:
                    gevent.spawn(self.callback_container.call, query)
            self.has_callback.clear()

    def _handle_commands(self, message: Message) -> bool:
        """Check message for commands in it.

        If there are commands, returns True and tries execute them
        Else returns False

        first_only bool
        when True will only consider first command in a message.
        """
        text = message.text or message.caption

        if not text:
            return False

        entities = message.entities or message.caption_entities

        if entities is None:
            return False

        # Collect commands from message
        commands = deque([
            (text[e.offset:e.offset+e.length], e.offset, e.offset+e.length)
            for e in entities
            if e.type == 'bot_command'
            and (e.offset == 0 or not self.first_only_command)
            ])

        if not commands:
            return False

        while commands:
            command, start, end = commands.popleft()
            if '@' in command:
                command, bot_name = command.split('@', 1)
                if bot_name != self.name:
                    continue

            # Parse arguments for each command
            try:
                if commands:
                    _, nxt_c, _ = commands[0]
                    args = [message] + shlex.split(text[end:nxt_c])
                else:
                    args = [message] + shlex.split(text[end:])
            except ValueError:
                args = [message, text[end:]]

            found = self.command_container.find_command(command)
            for method in found:
                bound_args = check_args(method, args)
                if bound_args is None:
                    self._call_listeners('on_command_failure', message)
                    continue
                try:
                    if not using_greenlets:
                        method(*bound_args.args, **bound_args.kwargs)
                    else:
                        gevent.spawn(
                            method,
                            *bound_args.args,
                            **bound_args.kwargs
                            )
                except Exception as err:
                    logger.exception(f"Exception on command {repr(command)}")
                    self._call_listeners('on_command_failure', message, err)
        return True

    def _handle_message(self, message: Message):
        """Process a single message"""
        if not self._handle_commands(message):
            self._call_listeners('on_plain_message', message)

        if message.left_chat_member is not None:
            self._call_listeners('on_left_chat_member', message)
        elif message.new_chat_members is not None:
            self._call_listeners('on_new_chat_members', message)

        if message.new_chat_title is not None:
            self._call_listeners('on_new_chat_title', message)

    def _call_listeners(self, event, *args, **kwargs):
        for listener in self.listeners:
            method = getattr(listener, event)
            if not using_greenlets:
                method(*args, **kwargs)
            else:
                gevent.spawn(method, *args, **kwargs)

    def _webhook_loop(self):
        class HandleUpdates(BaseHTTPRequestHandler):
            bot = self

            def _set_headers(self):
                self.send_response(200)
                self.end_headers()

            def do_POST(self):
                '''Reads post request body'''
                self._set_headers()
                content_len = int(self.headers.get('content-length', 0))
                post_body = self.rfile.read(content_len).decode()
                update = Update.from_json(post_body)
                HandleUpdates.bot.process_update(update)

        HTTPServer((self.webhook, 443), HandleUpdates).serve_forever()


__all__ = [OrigamiBot.__name__]
