from .base import TelegramStructure, Field
from .order_info import OrderInfo


class SuccessfulPayment(TelegramStructure):

    currency = Field()
    total_amount = Field()
    invoice_payload = Field()
    telegram_payment_charge_id = Field()
    provider_payment_charge_id = Field()
    shipping_option_id = Field()
    order_info = Field()

    def __init__(self,
                 currency: str,
                 total_amount: int,
                 invoice_payload: str,
                 telegram_payment_charge_id: str,
                 provider_payment_charge_id: str,
                 shipping_option_id: str = None,
                 order_info: OrderInfo = None
                 ):

        self.currency = \
            Field(currency, [str])

        self.total_amount = \
            Field(total_amount, [int])

        self.invoice_payload = \
            Field(invoice_payload, [str])

        self.telegram_payment_charge_id = \
            Field(telegram_payment_charge_id, [str])

        self.provider_payment_charge_id = \
            Field(provider_payment_charge_id, [str])

        self.shipping_option_id = \
            Field(shipping_option_id, [str])

        self.order_info =\
            Field(order_info, [OrderInfo])
