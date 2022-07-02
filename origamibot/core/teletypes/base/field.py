from logging import getLogger

logger = getLogger('origamibot')


class FieldTypeError(TypeError):
    pass


class Field:
    """Utility class for storing values in TelegramStructure,
    type checking and auto-mapping dicts to appropriate TelegramStructure

    Usual user does not interact with this class directly
    """

    __slots__ = ('_value', 'data_types', 'structures', 'possible_fields')

    def unfold(self):
        def unfold_list(l):
            return [
                unfold_list(i)
                if isinstance(i, list)
                else i.unfold()
                for i in l
            ]
        if isinstance(self.value, list):
            return unfold_list(self.value)
        elif isinstance(self.value, TelegramStructure):
            return self.value.unfold()
        return self.value

    def __init__(self, value=None, data_types=[]):
        self.data_types = set(data_types)

        # Add subclasses also
        for t in data_types:
            scls = t.__subclasses__()
            if not scls:
                continue
            for i in scls:
                self.data_types.add(i)

        self.structures = [
            i
            for i in data_types
            if issubclass(i, TelegramStructure)
            ]

        self.possible_fields = {
            field_name
            for tg_struct in self.structures
            for field_name in tg_struct.fields_names()
        }
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
                value = {
                    key: value
                    for key, value in value.items()
                    if key in self.possible_fields
                }
                for struct in self.structures:
                    try:
                        return struct.from_dict(value, value)
                        break
                    except TypeError as err:
                        logger.debug(
                            f'Error in Field, unpacking {struct}:\n\t{err}')
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
                if type(item) == dict:
                    try:
                        value[i] = struct.from_dict(item, None)
                    except TypeError as err:
                        logger.debug(
                            f'Error in Field, unpacking {struct}:\n\t{err}')
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
