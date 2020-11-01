from weakref import WeakMethod
from inspect import getmembers
from collections import deque
from logging import getLogger

logger = getLogger('origamibot')


class Callbacks:
    def __init__(self):
        self.callback_objs = []
        self.callback_methods = []

    def add(self, callback):
        self.callback_objs.append(callback)
        for c_name, c_call in getmembers(callback, lambda item: callable(item)):
            if c_name.startswith('_'):
                continue
            self.callback_methods.append(WeakMethod(c_call))

    def remove(self, callback):
        self.callback_objs.remove(callback)

    def call(self, query):
        que = deque(self.callback_methods)
        self.callback_methods = []
        while que:
            method_ref = que.popleft()
            method = method_ref()
            if method is None:
                continue
            try:
                method(query)
            except Exception:
                logger.exception(
                    'Exception while calling Inline query handler'
                    )
            self.callback_methods.append(method_ref)
