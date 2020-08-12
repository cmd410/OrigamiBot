from .base import TelegramStructure, Field


class Dice(TelegramStructure):

    emoji = Field()
    value = Field()

    def __init__(self,
                 emoji: str,
                 value: int
                 ):
        self.emoji = \
            Field(emoji, [str])

        self.value = \
            Field(value, [int])
