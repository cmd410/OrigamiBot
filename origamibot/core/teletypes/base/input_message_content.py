from .telegram_structure import TelegramStructure


class InputMessageContent(TelegramStructure):
    def __new__(cls, **kwargs):
        if cls != InputMessageContent:
            return cls(**kwargs)
        for i in InputMessageContent.__subclasses__():
            try:
                return i(**kwargs)
            except TypeError:
                pass
        raise TypeError(
            f'Could not determine InputMessageContent from {kwargs}'
            )