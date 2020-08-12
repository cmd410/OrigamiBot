from .telegram_structure import TelegramStructure
from .field import Field


class InputMedia(TelegramStructure):
    """Base class for InputMedia[whatever]
    """

    type = Field()
    media = Field()

    def __init__(self,
                 type: str,
                 media: str
                 ):
        self.type = \
            Field(type, [str])

        self.media = \
            Field(media, [str])
