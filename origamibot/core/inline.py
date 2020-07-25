from weakref import WeakMethod
from inspect import getmembers


class InlineCallbacks:
    def __init__(self):
        self.callback_objs = []
        self.callback_methods = []

    def add(self, callback):
        self.callback_objs.append(callback)
        for c_name, c_call in getmembers(callback, lambda item: callable(item)):
            if c_name.startswith('_'):
                continue
            self.callback_methods.append(WeakMethod(c_call))

    def call(self, query):
        for i in self.callback_methods:
            method = i()
            if method is None:
                continue
            try:
                method(query)
            except Exception as err:
                print(err)
