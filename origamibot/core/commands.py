from typing import List, Callable
from inspect import getmembers
from weakref import WeakMethod


class CommandContainer:
    """Class that contains objects that contain bot's commands as methods"""
    def __init__(self):
        self.command_holders = []
        self._cache = dict()

    def add_command(self, obj, cache=True):
        """Add object to command container."""
        self.command_holders.append(obj)

        if cache:
            for c_name, c_call in getmembers(obj, lambda item: callable(item)):
                if c_name.startswith('_'):
                    continue
                if c_name in self._cache.keys():
                    self._cache[c_name].append(self._make_weak(c_name, c_call))
                else:
                    self._cache[c_name] = [self._make_weak(c_name, c_call)]

    def remove(self, obj):
        self.command_holders.remove(obj)

    def remove_by_filter(self, filter_func: Callable):
        """Remove commands from container by filter

        Filter must be a callable with single argument(item)
        and should return True for each item that needs removing
        """
        removables = [
            i
            for i in self.command_holders
            if filter_func(i)
        ]

        for r in removables:
            self.command_holders.remove(r)

    def clear(self):
        """Remove all commands"""
        self.command_holders.clear()

    def find_command(self, command: str) -> List[Callable]:
        """Find a method for given command.

        Returns a list of all matched methods.
        """
        if command.startswith('/'):
            command = command[1:]

        if command in self._cache.keys():
            return [i() for i in self._cache[command]]

        # Do not look for protected/private methods
        if command.startswith('_'):
            return []

        matches = []
        for holder in self.command_holders:
            if hasattr(holder, command):
                command_handle = getattr(holder, command)
                if callable(command_handle):
                    matches.append(command_handle)

        self._cache[command] = [self._make_weak(command, i) for i in matches]
        return matches

    def _make_weak(self, command, method):
        """Make weak reference to command"""
        return WeakMethod(method, self._on_command_delete(command))

    def _on_command_delete(self, command: str):
        """Remove command from cache when its GCed"""
        def remove_from_cache(weak_reference):
            self._cache[command].remove(weak_reference)
        return remove_from_cache
