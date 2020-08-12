from .telegram_structure import TelegramStructure
from .field import Field


class InlineQueryResult(TelegramStructure):

    id = Field()
    type = Field()

    def __init__(self,
                 id: str,
                 type: str
                 ):
        self.id = \
            Field(id, [str])

        self.type = \
            Field(type, [str])
