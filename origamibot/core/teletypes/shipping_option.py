from typing import List

from .base import ListField, Field, TelegramStructure

from .labeled_price import LabeledPrice


class ShippingOption(TelegramStructure):

    id = Field()
    title = Field()
    prices = Field()

    def __init__(self,
                 id: str,
                 title: str,
                 prices: List[LabeledPrice]
                 ):
        self.id = \
            Field(id, [str])

        self.title = \
            Field(title, [str])

        self.prices = \
            ListField(prices, [LabeledPrice])
