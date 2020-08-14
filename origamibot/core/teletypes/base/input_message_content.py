from .telegram_structure import TelegramStructure


class InputMessageContent(TelegramStructure):
    def __new__(cls, **kwargs):
        if cls != InputMessageContent:
            return super(InputMessageContent, cls).__new__(cls)
        keys = set(kwargs.keys())
        for i in InputMessageContent.__subclasses__():
            if not keys.issubset(i.fields_names()):
                continue
            return super(InputMessageContent, i).__new__(i)
        raise TypeError(
            f'Could not determine InputMessageContent from {kwargs}'
            )