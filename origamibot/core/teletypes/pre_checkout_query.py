from .base import TelegramStructure, Field

from .user import User
from .order_info import OrderInfo


class PreCheckoutQuery(TelegramStructure):

    id = Field()
    from_user = Field()
    currency = Field()
    total_amount = Field()
    invoice_payload = Field()
    shipping_option_id = Field()
    order_info = Field()

    def __init__(self,
                 id: str,
                 from_user: User,
                 currency: str,
                 total_amount: int,
                 invoice_payload: str,
                 shipping_option_id: str = None,
                 order_info: OrderInfo = None
                 ):
        self.id = \
            Field(id, [str])

        self.from_user = \
            Field(from_user, [User])

        self.currency = \
            Field(currency, [str])

        self.total_amount = \
            Field(total_amount, [int])

        self.invoice_payload = \
            Field(invoice_payload, [str])

        self.shipping_option_id = \
            Field(shipping_option_id, [str])

        self.order_info = \
            Field(order_info, [OrderInfo])
