from typing import Any
from pydantic import BaseModel
from collections.abc import MutableMapping


class TelegramObject(BaseModel, MutableMapping[str, Any]):
    """Base telegram object pydantic model
    """
    class Config:
        extra = 'allow'

    def __getitem__(self, key: str):
        if key in self.__fields_set__:
            return getattr(self, key)
        raise KeyError(f'Field {key} not present in {self.__class__.__name__}')

    def __setitem__(self, key: str, value: Any):
        if key in self.__fields_set__:
            setattr(self, key, value)
        raise KeyError(f'Field {key} not present in {self.__class__.__name__}')

    def __delitem__(self, key: str):
        raise RuntimeError("Can't delete attribute of defined model!")

    def __iter__(self):
        for i in self.__fields_set__:
            yield i

    def __len__(self) -> int:
        return len(self.__fields_set__)
