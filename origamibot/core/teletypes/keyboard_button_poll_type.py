from .base import TelegramStructure, Field


class KeyboardButtonPollType(TelegramStructure):

    type = Field()

    def __init__(self, type: str):
        self.type = \
            Field(type, [str])
