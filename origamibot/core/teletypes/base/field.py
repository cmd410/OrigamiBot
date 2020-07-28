class FieldTypeError(TypeError):
    pass


class Field:
    """Utility class for storing values in TelegramStructure,
    type checking and auto-mapping dicts to appropriate TelegramStructure

    Usual user does not interact with this class directly
    """

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
        self.data_types = data_types
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
        if not self.data_types:
            return value
        if not (value is None and None in self.data_types):
            value_type = type(value)
            if value_type not in self.data_types:
                if value_type == dict:   # Auto convert dict to data structure
                    # Collect all possible structures
                    structures = [
                        i
                        for i in self.data_types
                        if issubclass(i, TelegramStructure)
                        or isinstance(i, str)
                    ]

                    for struct in structures:
                        if isinstance(struct, str):
                            # If structure is given by its name search in
                            # TelegramStructure subclasses
                            # It should not happend in 99% of times
                            # but just in case
                            for cls in TelegramStructure.__subclasses__():
                                if cls.__name__ == struct:
                                    struct = cls
                                    break
                            try:
                                return struct(**value)
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


from .telegram_structure import TelegramStructure  # NOQA
