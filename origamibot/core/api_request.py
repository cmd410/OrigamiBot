import requests
import json

from typing import List, Union, Optional, IO, Literal

from .exceptions import TelegramAPIError
from .teletypes import (
    TelegramStructure,
    Update,
    User,
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
    BotCommandScope
)

from .teletypes.inline_query_result import InlineQueryResult

try:
  from telegram_text.bases import Element
  
  def convert_elements_to_str(data: dict):
    """Convert telegram-text elements to jsonable text string
    and add appropriate parse_mode parameter if not present.
    """
    parse_mode = data.get("parse_mode", "HTML")
    for text_key in ("text", "caption"):
      text = data.get(text_key)
      if isinstance(text, Element):
        data["parse_mode"] = parse_mode
        if parse_mode == "HTML":
          data[text_key] = text.to_html()
        elif parse_mode in {"MarkdownV2", "Markdown"}:
          data[text_key] = text.to_markdown()
        break

except ImportError:
  class Element: ...  # fallback for type hints
  def convert_elements_to_str(_): pass  # noop if telegram-text is not present


api_url = 'https://api.telegram.org/bot{token}/{method}'


def request(token,
            method,
            data=dict(),
            files=dict(),
            excpect=None
            ) -> Union[TelegramStructure, List[TelegramStructure]]:
    """Make a raw api request.

    Returns result as dataclass or list of dataclasses
    """
    url = api_url.format(token=token, method=method)

    data = {
        key: value
        for key, value in data.items()
        if value is not None
    }
  
    convert_elements_to_str(data)

    files = {
        key: value
        for key, value in files.items()
        if value is not None
    }
    if files:
        response = requests.post(url, params=data, files=files)
    else:
        json_data = json.dumps(data, ensure_ascii=True)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)

    if response.status_code != 200:
        description = \
            json.loads(response.text).get('description', 'No description')
        raise TelegramAPIError(f'[{response.status_code}] {description}')

    data = json.loads(response.text)['result']

    if isinstance(data, dict):
        return TelegramStructure.from_dict(data)
    elif isinstance(data, list):
        return TelegramStructure.from_list(data)
    return data


def get_updates(token: str,
                offset: int = 0,
                limit: int = 100,
                timeout: int = 0,
                allowed_updates: list = []) -> List[Update]:
    """Make getUpdate request to telegram API. Return list of updates"""

    updates = request(
        token,
        'getUpdates',
        data={
            'offset': offset + 1,
            'limit': limit,
            'allowed_updates': allowed_updates,
            'timeout': timeout
            },
        excpect='update'
        )
    return updates


def get_me(token: str) -> User:
    """A simple method for testing your bot's auth token.

    Returns basic information about the bot in form of a User object.
    """
    return request(
        token,
        'getMe',
        excpect='user'
        )


def send_message(token: str,
                 chat_id: Union[int, str],
                 text: Union[str, Element],
                 parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
                 disable_web_page_preview: Optional[bool] = None,
                 disable_notification: Optional[bool] = None,
                 reply_to_message_id: Optional[int] = None,
                 reply_markup: Optional[ReplyMarkup] = None,
                 protect_content: Optional[bool] = None) -> Message:
    """Use this method to send text messages.

    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None else None),
            'protect_content': protect_content
        }
    return request(
        token,
        'sendMessage',
        data,
        excpect='message'
    )


def forward_message(token: str,
                    chat_id: Union[int, str],
                    from_chat_id: Union[int, str],
                    message_id: int,
                    disable_notification: Optional[bool] = None,
                    protect_content: Optional[bool] = None
                    ) -> Message:
    """Use this method to forward messages of any kind.

    On success, the sent Message is returned.
    """
    data = {
        'chat_id': chat_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id,
        'disable_notification': disable_notification,
        'protect_content': protect_content
    }

    return request(
        token,
        'forwardMessage',
        data,
        excpect='message'
    )


def send_photo(token: str,
               chat_id: Union[int, str],
               photo: Union[str, IO],
               caption: Union[str, Element, None] = None,
               parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None,
               protect_content: Optional[bool] = None
               ) -> Message:
    """Use this method to send photos.

    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None else None),
            'protect_content': protect_content
        }
    if not isinstance(photo, str):
        return request(token,
                       'sendPhoto',
                       data,
                       files={
                           'photo': photo
                       },
                       excpect='message')
    else:
        data['photo'] = photo
        return request(token,
                       'sendPhoto',
                       data,
                       excpect='message')


def send_audio(token: str,
               chat_id: Union[int, str],
               audio: Union[str, IO],
               caption: Union[str, Element, None] = None,
               parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
               duration: Optional[int] = None,
               performer: Optional[str] = None,
               title: Optional[str] = None,
               thumb: Optional[Union[str, IO]] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None,
               protect_content: Optional[bool] = None
               ) -> Message:
    """Use this method to send audio files.

    Your audio must be in the .MP3 or .M4A format.
    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'title': title,
            'performer': performer,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None else None),
            'protect_content': protect_content
        }
    files = dict()
    if isinstance(audio, str):
        data['audio'] = audio
    else:
        files['audio'] = audio

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendAudio',
        data,
        files
    )


def send_document(token: str,
                  chat_id: Union[int, str],
                  document: Union[str, IO],
                  thumb: Optional[Union[str, IO]] = None,
                  caption: Union[str, Element, None] = None,
                  parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
                  disable_notification: Optional[bool] = None,
                  reply_to_message_id: Optional[int] = None,
                  reply_markup: Optional[ReplyMarkup] = None,
                  protect_content: Optional[bool] = None
                  ) -> Message:
    """Use this method to send general files.

    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None else None),
            'protect_content': protect_content
        }

    files = dict()
    if isinstance(document, str):
        data['document'] = document
    else:
        files['document'] = document

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendDocument',
        data,
        files
    )


def send_video(token: str,
               chat_id: Union[int, str],
               video: Union[str, IO],
               duration: Optional[int] = None,
               width: Optional[int] = None,
               height: Optional[int] = None,
               thumb: Optional[Union[str, IO]] = None,
               caption: Union[str, Element, None] = None,
               parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
               supports_streaming: Optional[bool] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None,
               protect_content: Optional[bool] = None
               ) -> Message:
    """Use this method to send video files.

    Telegram clients support mp4 videos (other formats may be sent as Document)
    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'height': height,
            'width': width,
            'duration': duration,
            'parse_mode': parse_mode,
            'supports_streaming': supports_streaming,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None else None),
            'protect_content': protect_content
        }

    files = dict()
    if isinstance(video, str):
        data['video'] = video
    else:
        files['video'] = video

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendVideo',
        data,
        files
    )


def send_animation(token: str,
                   chat_id: Union[int, str],
                   animation: Union[str, IO],
                   duration: Optional[int] = None,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   thumb: Optional[Union[str, IO]] = None,
                   caption: Optional[Union[str, IO]] = None,
                   parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None,
                   protect_content: Optional[bool] = None
                   ) -> Message:
    """Use this method to send animation files (GIF or video without sound).

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'duration': duration,
        'width': width,
        'height': height,
        'caption': caption,
        'parse_mode': parse_mode,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': (reply_markup.unfold()
                         if reply_markup is not None else None),
        'protect_content': protect_content
    }

    files = dict()
    if isinstance(animation, str):
        data['animation'] = animation
    else:
        files['animation'] = animation

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendAnimation',
        data,
        files
    )


def send_voice(token: str,
               chat_id: Union[int, str],
               voice: Union[str, IO],
               caption: Union[str, Element, None] = None,
               parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
               duration: Optional[int] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None,
               protect_content: Optional[bool] = None
               ) -> Message:
    """Use this method to send audio files to display the file as a voice message.

    For this to work, your audio must be in an .OGG file encoded with OPUS.
    On success, the sent Message is returned.
    """
    data = {
        'chat_id': chat_id,
        'duration': duration,
        'caption': caption,
        'parse_mode': parse_mode,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': (reply_markup.unfold()
                         if reply_markup is not None else None),
        'protect_content': protect_content
    }

    files = dict()
    if isinstance(voice, str):
        data['voice'] = voice
    else:
        files['voice'] = voice

    return request(
        token,
        'sendVoice',
        data,
        files,
        excpect='message'
    )


def send_video_note(token: str,
                    chat_id: Union[int, str],
                    video_note: Union[str, IO],
                    duration: Optional[int] = None,
                    length: Optional[int] = None,
                    thumb: Optional[Union[str, IO]] = None,
                    disable_notification: Optional[bool] = None,
                    reply_to_message_id: Optional[int] = None,
                    reply_markup: Optional[ReplyMarkup] = None,
                    protect_content: Optional[bool] = None
                    ) -> Message:
    """Use this method to send rounded square mp4 videos of up to 1 minute long.

    On success, the sent Message is returned."""
    data = {
            'chat_id': chat_id,
            'duration': duration,
            'length': length,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None else None),
            'protect_content': protect_content
        }

    files = dict()
    if isinstance(video_note, str):
        data['video_note'] = video_note
    else:
        files['video_note'] = video_note

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendVideoNote',
        data,
        files,
        excpect='message'
    )


def send_location(token: str,
                  chat_id: Union[int, str],
                  latitude: float,
                  longitude: float,
                  live_period: Optional[int] = None,
                  disable_notification: Optional[bool] = None,
                  reply_to_message_id: Optional[int] = None,
                  reply_markup: Optional[ReplyMarkup] = None,
                  protect_content: Optional[bool] = None
                  ) -> Message:
    """Use this method to send point on the map.

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'live_period': live_period,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup.unfold(),
        'protect_content': protect_content
    }

    return request(
        token,
        'sendLocation',
        data,
        excpect='message'
    )


def edit_message_live_location(token: str,
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
    data = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup.unfold()
    }

    return request(
        token,
        'editMessageLiveLocation',
        data,
        excpect='message'
    )


def stop_message_live_location(token: str,
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

    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup.unfold()
    }

    return request(
        token,
        'stopMessageLiveLocation',
        data,
        excpect='message'
    )


def send_venue(token: str,
               chat_id: Union[int, str],
               latitude: float,
               longitude: float,
               title: str,
               address: str,
               foursquare_id: Optional[str] = None,
               foursquare_type: Optional[str] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None,
               protect_content: Optional[bool] = None
               ) -> Message:
    """Use this method to send information about a venue.

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'title': title,
        'address': address,
        'foursquare_id': foursquare_id,
        'foursquare_type': foursquare_type,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup.unfold(),
        'protect_content': protect_content
    }

    return request(
        token,
        'sendVenue',
        data,
        excpect='message'
    )


def send_contact(token: str,
                 chat_id: Union[int, str],
                 phone_number: str,
                 first_name: str,
                 last_name: Optional[str] = None,
                 vcard: Optional[str] = None,
                 disable_notification: Optional[bool] = None,
                 reply_to_message_id: Optional[int] = None,
                 reply_markup: Optional[ReplyMarkup] = None,
                 protect_content: Optional[bool] = None
                 ) -> Message:
    """Use this method to send phone contacts.

    On success, the sent Message is returned.
    """
    data = {
        'chat_id': chat_id,
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'vcard': vcard,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup.unfold(),
        'protect_content': protect_content
    }

    return request(
        token,
        'sendContact',
        data,
        excpect='message'
    )


def send_poll(token: str,
              chat_id: Union[int, str],
              question: str,
              options: List[str],
              is_anonymous: Optional[bool] = None,
              type: Optional[str] = None,
              allows_multiple_answers: Optional[bool] = None,
              correct_option_id: Optional[int] = None,
              explanation: Optional[str] = None,
              explanation_parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
              open_period: Optional[int] = None,
              close_date: Optional[int] = None,
              is_closed: Optional[bool] = None,
              disable_notification: Optional[bool] = None,
              reply_to_message_id: Optional[int] = None,
              reply_markup: Optional[ReplyMarkup] = None,
              protect_content: Optional[bool] = None
              ) -> Message:
    """Use this method to send a native poll.

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'question': question,
        'options': options,
        'is_anonymous': is_anonymous,
        'type': type,
        'allows_multiple_answers': allows_multiple_answers,
        'correct_option_id': correct_option_id,
        'explanation': explanation,
        'explanation_parse_mode': explanation_parse_mode,
        'open_period': open_period,
        'close_date': close_date,
        'is_closed': is_closed,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup.unfold(),
        'protect_content': protect_content
    }

    return request(
        token,
        'sendPoll',
        data,
        excpect='message'
    )


def send_dice(token: str,
              chat_id: Union[int, str],
              emoji: Optional[str] = None,
              disable_notification: Optional[bool] = None,
              reply_to_message_id: Optional[int] = None,
              reply_markup: Optional[ReplyMarkup] = None,
              protect_content: Optional[bool] = None
              ) -> Message:
    """Use this method to send an animated emoji that will display a random value.

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'emoji': emoji,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup.unfold(),
        'protect_content': protect_content
    }

    return request(
        token,
        'sendDice',
        data,
        excpect='message'
    )


def send_chat_action(token: str,
                     chat_id: Union[int, str],
                     action: str
                     ) -> bool:
    """Use this method to tell that something is happening on the bot's side.

    The status is set for 5 seconds or less,
    when a message arrives from your bot, clients clear its typing status

    Returns True on success.
    """
    return request(
        token,
        'sendChatAction',
        {
            'chat_id': chat_id,
            'action': action
        }
    )


def get_user_profile_photos(token: str,
                            user_id: int,
                            offset: Optional[int] = None,
                            limit: Optional[int] = None
                            ) -> UserProfilePhotos:
    """Use this method to get a list of profile pictures for a user.

    Returns a UserProfilePhotos object.
    """
    return request(
        token,
        'getUserProfilePhotos',
        {
            'user_id': user_id,
            'offset': offset,
            'limit': limit
        }
    )


def kick_chat_member(token: str,
                     chat_id: Union[int, str],
                     user_id: int,
                     until_date: Optional[int] = None
                     ) -> bool:
    """Use this method to kick a user from a group, a supergroup or a channel.

    The bot must be an administrator in the chat for this to work
    and must have the appropriate admin rights.

    Returns True on success.
    """
    return request(
        token,
        'kickChatmember',
        {
            'chat_id': chat_id,
            'user_id': user_id,
            'until_date': until_date
        }
    )


def unban_chat_member(token: str,
                      chat_id: Union[int, str],
                      user_id: int
                      ) -> bool:
    """Use this method to unban
    a previously kicked user in a supergroup or channel.

    Returns True on success.
    """
    return request(
        token,
        'unbanChatMember',
        {
            'chat_id': chat_id,
            'user_id': user_id
        }
    )


def restrict_chat_member(token: str,
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
    data = {
        'chat_id': chat_id,
        'user_id': user_id,
        'permissions': permissions.unfold(),
        'until_date': until_date
    }

    return request(
        token,
        'restrictChatMember',
        data
    )


def promote_chat_member(token: str,
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

    data = {
        'chat_id': chat_id,
        'user_id': user_id,
        'can_change_info': can_change_info,
        'can_post_messges': can_post_messages,
        'can_edit_messages': can_edit_messages,
        'can_delete_messages': can_delete_messages,
        'can_invite_users': can_invite_users,
        'can_restrict_users': can_restrict_members,
        'can_pin_messages': can_pin_messages,
        'can_promote_members': can_promote_members
    }

    return request(
        token,
        'promoteChatMember',
        data
    )


def set_chat_administrator_custom_title(token: str,
                                        chat_id: Union[int, str],
                                        user_id: int,
                                        custom_title: int
                                        ) -> bool:
    """Use this method to set a custom title for an administrator
    in a supergroup promoted by the bot.

    Returns True on success."""

    return request(
        token,
        'setChatAdministratorCustomTitle',
        {
            'chat_id': chat_id,
            'user_id': user_id,
            'custom_title': custom_title
        }
    )


def set_chat_permissions(token: str,
                         chat_id: Union[int, str],
                         permissions: ChatPermissions
                         ) -> bool:
    """Use this method to set default chat permissions for all members.

    The bot must be an administrator in the group or a supergroup
    for this to work and must have the can_restrict_members admin rights.

    Returns True on success.
    """
    return request(
        token,
        'setChatPermissions',
        {
            'chat_id': chat_id,
            'permissions': permissions.unfold()
        }
    )


def export_chat_invite_link(token: str,
                            chat_id: Union[int, str]
                            ) -> str:
    """Use this method to generate a new invite link for a chat;
    any previously generated link is revoked.

    Returns the new invite link as String on success.
    """
    return request(
        token,
        'exportChatInviteLink',
        {
            'chat_id': chat_id
        }
    )


def set_chat_photo(token: str,
                   chat_id: Union[int, str],
                   photo: IO
                   ) -> bool:
    """Use this method to set a new profile photo for the chat.

    Returns True on success.
    """
    return request(
        token,
        'setChatPhoto',
        {
            'chat_id': chat_id
        },
        {
            'photo': photo
        }
    )


def delete_chat_photo(token: str,
                      chat_id: Union[int, str]
                      ) -> bool:
    """Use this method to delete a chat photo.

    Returns True on success.
    """
    return request(
        token,
        'deleteChatPhoto',
        {
            'chat_id': chat_id
        }
    )


def set_chat_title(token: str,
                   chat_id: Union[int, str],
                   title: str
                   ) -> bool:
    """Use this method to change the title of a chat.

    Returns True on success.
    """
    return request(
        token,
        'setChatTitle',
        {
            'chat_id': chat_id,
            'title': title
        }
    )


def set_chat_description(token: str,
                         chat_id: Union[int, str],
                         description: Optional[str] = None
                         ) -> bool:
    """Use this method to change the description of a group,
    a supergroup or a channel.

    Returns True on success.
    """

    return request(
        token,
        'setChatDescription',
        {
            'chat_id': chat_id,
            'description': description
        }
    )


def pin_chat_message(token: str,
                     chat_id: Union[int, str],
                     message_id: int,
                     disable_notification: Optional[bool] = None
                     ) -> bool:
    """Use this method to pin a message in a group, a supergroup, or a channel.

    Returns True on success.
    """
    return request(
        token,
        'pinChatMessage',
        {
            'chat_id': chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification
        }
    )


def unpin_chat_message(token: str,
                       chat_id: Union[int, str]
                       ) -> bool:
    """Use this method to unpin a message in a group, a supergroup, or a channel.

    Returns True on success.
    """
    return request(
        token,
        'unpinChatMessage',
        {
            'chat_id': chat_id
        }
    )


def leave_chat(token: str,
               chat_id: Union[int, str]
               ) -> bool:
    """Use this method for your bot to leave a group, supergroup or channel.

    Returns True on success.
    """
    return request(
        token,
        'leaveChat',
        {
            'chat_id': chat_id
        }
    )


def get_chat(token: str,
             chat_id: Union[int, str]
             ) -> Chat:
    """Use this method to get up to date information about the chat.

    Returns a Chat object on success.
    """
    return request(
        token,
        'getChat',
        {
            'chat_id': chat_id
        }
    )


def get_chat_administrators(token: str,
                            chat_id: Union[int, str],
                            ) -> List[ChatMember]:
    """Use this method to get a list of administrators in a chat.

    On success, returns an Array of ChatMember objects
    that contains information about all chat administrators
    except other bots.
    """
    return request(
        token,
        'getChatAdministrators',
        {
            'chat_id': chat_id
        }
    )


def get_chat_members_count(token: str,
                           chat_id: Union[int, str]
                           ) -> int:
    """Use this method to get the number of members in a chat.

    Returns Int on success.
    """
    return request(
        token,
        'getChatMembersCount',
        {
            'chat_id': chat_id
        }
    )


def get_chat_member(token: str,
                    chat_id: Union[int, str],
                    user_id: int
                    ) -> ChatMember:
    """Use this method to get information about a member of a chat.

    Returns a ChatMember object on success.
    """
    return request(
        token,
        'getChatMember',
        {
            'chat_id': chat_id,
            'user_id': user_id
        }
    )


def set_chat_sticker_set(token: str,
                         chat_id: Union[int, str],
                         sticker_set_name: str
                         ) -> bool:
    """Use this method to set a new group sticker set for a supergroup

    Returns True on success.
    """
    return request(
        token,
        'setChatStickerSet',
        {
            'chat_id': chat_id,
            'sticker_set_name': sticker_set_name
        }
    )


def delete_chat_sticker_set(token: str,
                            chat_id:  Union[int, str]
                            ) -> bool:
    """Use this method to delete a group sticker set from a supergroup.

    Returns True on success.
    """
    return request(
        token,
        'deleteChatStickerSet',
        {
            'chat_id': chat_id
        }
    )


def answer_callback_query(token: str,
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
    return request(
        token,
        'answerCallbackQuery',
        {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'url': url,
            'cache_time': cache_time
        }
    )


def set_my_commands(token: str,
                    commands: List[BotCommand],
                    scope: Optional[BotCommandScope] = None,
                    language_code: Optional[str] = None
                    ) -> bool:
    """Use this method to change the list of the bot's commands.

    Returns True on success.
    """
    return request(
        token,
        'setMyCommands',
        {
            'commands': [i.unfold() for i in commands],
            'scope': scope.unfold() if scope else None,
            'language_code': language_code
        }
    )


def get_my_commands(token: str,
                    scope: Optional[BotCommandScope] = None,
                    language_code: Optional[str] = None
                    ) -> List[BotCommand]:
    """Use this method to get the current list of the bot's commands.

    Returns Array of BotCommand on success.
    """
    return request(
        token,
        'getMyCommands',
        {
            'scope': scope.unfold() if scope else None,
            'language_code': language_code
        }
    )


def delete_my_commands(token: str,
                       scope: Optional[BotCommandScope] = None,
                       language_code: Optional[str] = None
                       ) -> bool:
    """Use this method to delete the list of the bot's
    commands for the given scope and user language.
    After deletion, higher level commands will be shown
    to affected users.
    
    Returns True on success.
    """
    return request(
        token,
        'deleteMyCommands',
        {
            'scope': scope.unfold() if scope else None,
            'language_code': language_code
        }
    )


def answer_inline_query(token: str,
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
    return request(
        token,
        'answerInlineQuery',
        {
            'inline_query_id': inline_query_id,
            'results': [i.unfold() for i in results],
            'cache_time': cache_time,
            'is_personal': is_personal,
            'next_offset': next_offset,
            'switch_pm_text': switch_pm_text,
            'switch_pm_parameter': switch_pm_parameter
        }
    )


def set_webhook(token: str,
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
    return request(
        token,
        'setWebhook',
        {
            'url': url,
            'certificate': certificate,
            'max_connections': max_connections,
            'allowed_updates': allowed_updates
        }
    )


def delete_webhook(token: str):
    """Use this method to remove webhook integration
    if you decide to switch back to getUpdates.

    Returns True on success.
    """
    return request(
        token,
        'deleteWebhook'
    )


def get_webhook_info(token: str) -> WebhookInfo:
    """Use this method to get current webhook status.

    On success, returns a WebhookInfo object.
    If the bot is using getUpdates,
    will return an object with the url field empty.
    """
    return request(
        token,
        'getWebhookInfo'
    )


def edit_message_text(token: str,
                      chat_id: Union[int, str],
                      text: Union[str, Element],
                      message_id: Optional[int] = None,
                      inline_message_id: Optional[str] = None,
                      parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
                      disable_web_page_preview: Optional[bool] = None,
                      reply_markup: Optional[InlineKeyboardMarkup] = None
                      ) -> Union[Message, bool]:
    """Use this method to edit text and game messages.

    On success, if edited message is sent by the bot,
    the edited Message is returned,
    otherwise True is returned.
    """
    assert any([message_id, inline_message_id])
    return request(
        token,
        'editMessageText',
        {
            'chat_id': chat_id,
            'text': text,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview,
            'reply_markup': (reply_markup.unfold()
                             if reply_markup is not None
                             else None)
        }
    )


def edit_message_caption(token: str,
                         chat_id: Union[int, str],
                         caption: Union[str, Element, None] = None,
                         message_id: Optional[int] = None,
                         inline_message_id: Optional[str] = None,
                         parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
                         reply_markup: Optional[InlineKeyboardMarkup] = None
                         ) -> Union[Message, bool]:
    """Use this method to edit captions of messages.

    On success, if edited message is sent by the bot,
    the edited Message is returned,
    otherwise True is returned.
    """
    return request(
        token,
        'editMessageCaption',
        {
            'chat_id': chat_id,
            'caption': caption,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.unfold()
        }
    )


def edit_message_media(token: str,
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
    media_data, files = media.get_data_n_files()

    data = {
        'chat_id': chat_id,
        'media': media_data,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup.unfold()
    }

    return request(
        token,
        'editMessageMedia',
        data,
        files
    )


def edit_message_reply_markup(token: str,
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
    return request(
        token,
        'editMessageReplyMarkup',
        {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'reply_markup': reply_markup.unfold()
        }
    )


def stop_poll(token: str,
              chat_id: Union[int, str],
              message_id: int,
              reply_markup: Optional[InlineKeyboardMarkup] = None
              ) -> Poll:
    """Use this method to stop a poll which was sent by the bot.

    On success, the stopped Poll with the final results is returned.
    """
    return request(
        token,
        'stopPoll',
        {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': reply_markup.unfold()
        }
    )


def delete_message(token: str,
                   chat_id: Union[int, str],
                   message_id: int
                   ) -> bool:
    """Use this method to delete a message, including service messages

    Returns True on success.
    """
    return request(
        token,
        'deleteMessage',
        {
            'chat_id': chat_id,
            'message_id': message_id
        }
    )


def send_media_group(token: str,
                     chat_id: Union[int, str],
                     media: List[InputMedia],
                     disable_notification: Optional[bool] = None,
                     reply_to_message_id: Optional[bool] = None,
                     protect_content: Optional[bool] = None
                     ) -> Message:
    """Use this method to send a group of photos or videos as an album.
    On success, an array of the sent Messages is returned
    """
    assert 10 >= len(media) >= 2, 'Invalid number of media, must be 2-10'

    data = {
        'chat_id': chat_id,
        'media': [m.unfold() for m in media],
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'protect_content': protect_content
    }

    files = dict()
    for media_item in media:
        attach_name, file_path = media_item.file
        if not all([attach_name, file_path]):
            continue
        files[attach_name] = file_path

    return request(
        token,
        'sendMediaGroup',
        data,
        files,
        'message'
    )
