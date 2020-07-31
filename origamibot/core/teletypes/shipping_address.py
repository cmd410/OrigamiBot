from .base import TelegramStructure, Field


class ShippingAddress(TelegramStructure):

    country_code = Field()
    state = Field()
    city = Field()
    street_line1 = Field()
    street_line2 = Field()
    post_code = Field()

    def __init__(self,
                 country_code: str,
                 state: str,
                 city: str,
                 street_line1: str,
                 street_line2: str,
                 post_code: str
                 ):
        self.country_code = \
            Field(country_code, [str])

        self.state = \
            Field(state, [str])

        self.city = \
            Field(city, [str])

        self.street_line1 = \
            Field(street_line1, [str])

        self.street_line2 = \
            Field(street_line2, [str])

        self.post_code = \
            Field(post_code, [str])
