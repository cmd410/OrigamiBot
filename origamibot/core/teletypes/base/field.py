class FieldTypeError(TypeError):
    pass


class Field:
    """Utility class for storing values in TelegramStructure,
    type checking and auto-mapping dicts to appropriate TelegramStructure

    Usual user does not interact with this class directly
    """

    __slots__ = ('_value', 'data_types', 'structures')

    def unfold(self):
        if isinstance(self.value, list):
            return [
                i.unfold()
                for i in self.value
            ]
        elif isinstance(self.value, TelegramStructure):
            return self.value.unfold()
        return self.value

    def __init__(self, value=None, data_types=[]):
        self.data_types = set(data_types)
        self.structures = [
            i
            for i in data_types
            if issubclass(i, TelegramStructure)
            ]
        value = self.validate_value(value)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = self.validate_value(value)
        self._value = value

    def validate_value(self, value):
        """Check the type of value assigned,
        convert dict to structure if needed
        """
        if value is None:
            return value
        if not self.data_types:
            return value

        value_type = type(value)
        if value_type not in self.data_types:
            if value_type == dict and self.structures:
                if 'from' in value.keys():
                    value['from_user'] = value.pop('from')
                # Map dict to structures
                for struct in self.structures:
                    try:
                        return struct(**value)
                        break
                    except TypeError:
                        pass
            raise FieldTypeError(
                f'''Got wrong type: {
                    type(value)} expected one of {self.data_types}''')
        return value

    def __repr__(self):
        return f'<Field | {self.type.__name__} | {self.value}>'

    def __str__(self):
        return str(self.value)

    @property
    def type(self):
        return type(self.value)


class ListField(Field):
    def validate_value(self, value):
        if value is None:
            return value

        if not isinstance(value, list):
            raise FieldTypeError(
                f'''Got wrong type: {
                    type(value)} expected list of {self.data_types}''')
        if not value:
            return value

        for i, item in enumerate(value):
            item_type = type(item)
            if item_type in self.data_types:
                continue
            elif item_type == dict and self.structures:
                # Map dicts to structures
                for struct in self.structures:
                    try:
                        value[i] = struct(**item)
                        break
                    except TypeError:
                        pass
                if type(value[i]) == dict:
                    raise FieldTypeError(
                        f'''Can\'t map dict {
                            item} to any stucture in {
                                self.structures}'''
                        )
            elif item_type == list:
                # Convert nested lists
                value[i] = self.validate_value(item)
            else:
                raise FieldTypeError(
                    f'''Wrong type in list {
                        item}, excpected one of {
                            self.datatypes}'''
                    )

        return value



from .telegram_structure import TelegramStructure  # NOQA
