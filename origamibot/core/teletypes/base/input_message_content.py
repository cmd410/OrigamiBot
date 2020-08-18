from .telegram_structure import TelegramStructure


class InputMessageContent(TelegramStructure):
    def __new__(cls, *args, **kwargs):
        if cls != InputMessageContent:
            return super(InputMessageContent, cls).__new__(cls)
        keys = set(kwargs.keys())

        if not kwargs:
            raise ValueError('No keyword argumets given to determine type')
        classes = InputMessageContent.__subclasses__()
        classes = sorted(
            classes,
            key=lambda item: len(item.fields_names()),
            reverse=True
            )
        for i in classes:
            if not keys.issubset(i.fields_names()):
                continue
            return super(InputMessageContent, i).__new__(i)
        raise TypeError(
            f'Could not determine InputMessageContent from {kwargs}'
            )