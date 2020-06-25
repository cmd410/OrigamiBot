import shlex

from collections import deque
from threading import current_thread, Event
from time import sleep

from .sthread import StoppableThread
from .api_request import request
from .teletypes import Update, Message
from .commands import CommandContainer
from .util import check_args


class OrigamiBot:
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

    def send_message():
        pass

    def start(self):
        '''Start listening for updates. Non-blocking!'''
        self._listen_thread.start()
        self._process_thread.start()

    def stop(self):
        '''Terminate listening thread'''
        if self._listen_thread.is_alive():
            self._listen_thread.stop()
            self._listen_thread.join()
            self._process_thread.stop()
            self._process_thread.join()

    def process_update(self, update: Update):
        if update.message is not None:
            self._handle_message(update.message)

    def add_commands(self, obj):
        self.command_container.add_command(obj)

    def get_updates(self):
        '''Return list of updates'''
        updates = request(
            self.token,
            'getUpdates',
            data={'offset': self._last_update_id + 1}
            )
        if updates:
            self._last_update_id = updates[-1].update_id
        return updates

    def _process_updates_loop(self):
        while True:
            self.has_updates.wait()
            while self.updates:
                self.process_update(self.updates.popleft())
            self.has_updates.clear()

    def _listen_loop(self):
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
        text = message.text or message.caption

        if not text:
            return False

        entities = message.entities or message.caption_entities

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
                method(*bound_args.args, **bound_args.kwargs)
        return True

    def _handle_message(self, message: Message):
        if self._handle_commands(message):
            return
