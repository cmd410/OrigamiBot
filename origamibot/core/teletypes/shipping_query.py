from .base import Field, TelegramStructure

from .user import User
from .shipping_address import ShippingAddress


class ShippingQuery(TelegramStructure):

    id = Field()
    from_user = Field()
    invoice_payload = Field()
    shipping_address = Field()

    def __init__(self,
                 id: str,
                 from_user: User,
                 invoice_payload: str,
                 shipping_address: ShippingAddress
                 ):
        self.id = \
            Field(id, [str])

        self.from_user = \
            Field(from_user, [User])

        self.invoice_payload = \
            Field(invoice_payload, [str])

        self.shipping_address = \
            Field(shipping_address, [ShippingAddress])
