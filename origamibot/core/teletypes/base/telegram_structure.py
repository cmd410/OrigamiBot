import json
from logging import getLogger
from types import SimpleNamespace

from .field import Field

logger = getLogger('origamibot')


class TelegramStructure:
    def __getattribute__(self, name):
        item = object.__getattribute__(self, name)
        if isinstance(item, Field):
            return item.value
        return item

    def __setattr__(self, name, value):
        if name not in self.__dict__:
            object.__setattr__(self, name, value)

        item = object.__getattribute__(self, name)
        is_field = isinstance(item, Field)
        is_value_field = isinstance(value, Field)

        if is_field and not is_value_field:
            item.value = value
        else:
            object.__setattr__(self, name, value)

    def __repr__(self):
        s = f'{self.__class__.__name__}('
        s += ', '.join([
            f'{key}={repr(value.value)}'
            for key, value in self.raw_fields().items()
            if value.value is not None])
        s += ')'
        return s

    @classmethod
    def fields_names(cls):
        return {
            name
            for name, value in cls.__dict__.items()
            if isinstance(value, Field)
            }

    def raw_fields(self):
        """Retrun dict of raw Field objects in current instance"""
        return {
            key: value
            for key, value in self.__dict__.items()
            if isinstance(value, Field)
        }

    def unfold(self):
        """Returns a dictionary of not-None structure fields
        """
        d = dict()
        for key, value in self.__dict__.items():
            if not isinstance(value, Field):
                continue
            if value.value is not None:
                d[key] = value.unfold()
        return d

    def to_json(self):
        """Returns json string representing of this structure
        """
        return json.dumps(self.unfold())

    @classmethod
    def from_dict(cls, d: dict, valid_params = None):
        if 'from' in d.keys():
            d['from_user'] = d.pop('from')

        # Collect subclasses and their fields
        classes = [
            (c, c.fields_names())
            for c in cls.__subclasses__()
        ]

        # Sort so the fattest classes are first
        classes = sorted(
            classes,
            key=lambda item: len(item[1]),
            reverse=True
            )
        if valid_params is None:
            if cls != TelegramStructure:
                classes.append((cls, cls.fields_names()))

            valid_params = {
                key: value
                for c in classes
                for key, value in d.items()
                if key in c[1]
            }

        if cls != TelegramStructure:
            classes.append((cls, cls.fields_names()))

        d_keys = set(valid_params.keys())
        for c, fields in classes:
            if d_keys.issubset(fields):
                try:
                    return c(**valid_params)
                except TypeError:
                    raise
        logger.warning(f'Could not map dict: {d} to any type')
        return SimpleNamespace(**d)

    @classmethod
    def from_list(cls, l: list):  # NOQA
        new_list = []
        for i in l:
            if isinstance(i, dict):
                obj = cls.from_dict(i)
                new_list.append(obj)
            elif isinstance(i, list):
                obj = cls.from_list(i)
                new_list.append(obj)
            else:
                new_list.append(i)
        return new_list

    @classmethod
    def from_json(cls, json_string: str):
        if not json_string:
            raise ValueError("No json string given")
        data = json.loads(json_string)

        if isinstance(data, dict):
            return cls.from_dict(data)
        elif isinstance(data, list):
            return cls.from_list(data)
        else:
            raise TypeError(f'Cannot map {type(data)} to TelegramStructure')
