from .base import TelegramStructure, Field


class Invoice(TelegramStructure):

    title = Field()
    description = Field()
    start_parameter = Field()
    currency = Field()
    total_amount = Field()

    def __init__(self,
                 title: str,
                 description: str,
                 start_parameter: str,
                 currency: str,
                 total_amount: int
                 ):
        self.title = \
            Field(title, [str])

        self.description = \
            Field(description, [str])

        self.start_parameter = \
            Field(start_parameter, [str])

        self.currency = \
            Field(currency, [str])

        self.total_amount = \
            Field(total_amount, [int])
