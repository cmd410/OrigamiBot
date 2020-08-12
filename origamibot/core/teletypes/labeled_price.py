from .base import TelegramStructure, Field


class LabeledPrice(TelegramStructure):

    label = Field()
    amount = Field()

    def __init__(self,
                 label: str,
                 amount: int
                 ):
        self.label = \
            Field(label, [str])

        self.amount = \
            Field(amount, [int])
