from .base import TelegramStructure, Field
from .shipping_address import ShippingAddress


class OrderInfo(TelegramStructure):

    name = Field()
    phone_number = Field()
    email = Field()
    shipping_address = Field()

    def __init__(self,
                 name: str = None,
                 phone_number: str = None,
                 email: str = None,
                 shipping_address: ShippingAddress = None
                 ):

        self.name = \
            Field(name, [str])

        self.phone_number = \
            Field(phone_number, [str])

        self.email = \
            Field(email, [str])

        self.shipping_address = \
            Field(shipping_address, [ShippingAddress])
