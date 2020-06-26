import shlex

from typing import List, Optional, Union, IO
from collections import deque
from threading import current_thread, Event
from time import sleep

from .sthread import StoppableThread
from .teletypes import (
    Update,
    Message,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply)
from .commands import CommandContainer
from .util import check_args
from .api_request import (get_updates,
                          get_me,
                          send_message,
                          forward_message,
                          send_photo)


class OrigamiBot:
    """Telegram bot class."""
    def __init__(self, token):
        self.token = token
        self.updates = deque()
        self.interval = 0.1

        self._listen_thread = StoppableThread(
            name='Listen thread',
            target=self._listen_loop,
            daemon=True)
        
        self._process_thread = StoppableThread(
            name='Update process thread',
            target=self._process_updates_loop,
            daemon=True)

        self.has_updates = Event()

        self._last_update_id = 0

        self.command_container = CommandContainer()

    def start(self):
        """Start listening for updates. Non-blocking!"""
        self._listen_thread.start()
        self._process_thread.start()

    def stop(self):
        """Terminate all bot's threads."""
        if self._listen_thread.is_alive():
            self._listen_thread.stop()
            self._listen_thread.join()
            self._process_thread.stop()
            self._process_thread.join()

    def process_update(self, update: Update):
        """Process a single update."""
        if update.message is not None:
            self._handle_message(update.message)

    def add_commands(self, obj):
        """Add an object to bot's commands container.

        Object's methods, not preceded with underscore
        will be considered bot's commands.
        """
        self.command_container.add_command(obj)

    def get_updates(self) -> List[Update]:
        """Make getUpdate request to telegram API. Return list of updates"""
        updates = get_updates(
            self.token,
            self._last_update_id,
        )
        if updates:
            self._last_update_id = updates[-1].update_id
        return updates

    def get_me(self):
        return get_me(self.token)

    def send_message(self,
                     chat_id: Union[int, str],
                     text: str,
                     parse_mode: Optional[str] = None,
                     disable_web_page_preview: Optional[bool] = None,
                     disable_notification: Optional[bool] = None,
                     reply_to_message_id: Optional[int] = None) -> Message:
        """Use this method to send text messages.

        On success, the sent Message is returned.
        """
        return send_message(self.token,
                            chat_id,
                            text,
                            parse_mode,
                            disable_web_page_preview,
                            disable_notification,
                            reply_to_message_id)

    def forward_message(self,
                        chat_id: Union[int, str],
                        from_chat_id: Union[int, str],
                        message_id: int,
                        disable_notification: Optional[bool] = None) -> Message:
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
                   reply_markup: Optional[Union[
                        InlineKeyboardMarkup,
                        ReplyKeyboardMarkup,
                        ReplyKeyboardRemove,
                        ForceReply
                    ]] = None) -> Message:
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
        if current_thread().__class__.__name__ != '_MainThread':
            while True:
                if current_thread().stopped:
                    break
                updates = self.get_updates()
                if updates:
                    self.updates.extend(updates)
                    self.has_updates.set()
                sleep(self.interval)

    def _handle_commands(self, message: Message, first_only=False) -> bool:
        """Check message for commands in it.

        If there are commands, returns True and tries execute them
        Else returns False

        first_only bool when True will only consider first command in a message.
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
            and (e.offset == 0 or not first_only)
            ])

        if not commands:
            return False

        while commands:
            command, start, end = commands.popleft()

            # Parse arguments for each command
            if commands:
                _, nxt_c, _ = commands[0]
                args = [message] + shlex.split(text[end:nxt_c])
            else:
                args = [message] + shlex.split(text[end:])

            found = self.command_container.find_command(command)
            for method in found:
                bound_args = check_args(method, args)
                if bound_args is None:
                    continue
                try:
                    method(*bound_args.args, **bound_args.kwargs)
                except Exception as err:
                    print(err)   # TODO actual logging on failures with user defined commands

        return True

    def _handle_message(self, message: Message):
        """Process a single message"""
        if self._handle_commands(message):
            return
