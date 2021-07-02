import importlib as imp
import inspect
from pathlib import Path
from typing import Type

from ._base import TelegramObject
from .message import Message
from .user import User
from .update import Update
from .webhookinfo import WebhookInfo


def import_modules():
    d = Path(__file__).parent
    m = []
    
    for filepath in d.glob('[!_]*.py'):
        m.append(imp.import_module('.' + filepath.stem, __name__))
    
    return m


def collect_classes(modules):
    d = {}
    for m in modules:
        tg_objects = inspect.getmembers(
            m,
            predicate=lambda x: (inspect.isclass(x)
                                 and x is not TelegramObject
                                 and issubclass(x, TelegramObject))
            )
        d.update(dict(tg_objects))
    return d


def expose_forward_refs(modules: list, classes: dict[str, Type[TelegramObject]]):
    for name, cls in classes.items():
        for mod in modules:
            if cls.__module__ == mod.__name__:
                continue
            setattr(mod, name, cls)
    
    for i in classes.values():
        i.update_forward_refs()


modules = import_modules()
classes_map = collect_classes(modules)
expose_forward_refs(modules, classes_map)
