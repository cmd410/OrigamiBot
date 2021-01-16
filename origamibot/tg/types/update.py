from flowerfield import Field, OptionalField

from ._base import TelegramType


class Update(TelegramType):
    update_id            = Field(int)
    message              = OptionalField('Message')
    edited_message       = OptionalField('Message')
    channel_post         = OptionalField('Message')
    edited_channel_post  = OptionalField('Message')
    # TODO Update fields
    #inline_query         = OptionalField('InlineQuery')
    #chosen_inline_result = OptionalField('ChosenInlineResult')
    #callback_query       = OptionalField('CallbackQuery')
    #shipping_query       = OptionalField('ShippingQuery')
    #pre_checkout_query   = OptionalField('PreCheckoutQuery')
    #poll                 = OptionalField('Poll')
    #poll_answer          = OptionalField('PollAnswer')
