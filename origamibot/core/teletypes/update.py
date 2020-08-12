from .base import TelegramStructure, Field

from .message import Message
from .inline_query import InlineQuery
from .callback_query import CallbackQuery
from .shipping_query import ShippingQuery
from .pre_checkout_query import PreCheckoutQuery
from .poll import Poll
from .poll_answer import PollAnswer
from .chosen_inline_result import ChosenInlineResult


class Update(TelegramStructure):

    update_id = Field()
    message = Field()
    edited_message = Field()
    channel_post = Field()
    edited_channel_post = Field()
    inline_query = Field()
    chosen_inline_result = Field()
    callback_query = Field()
    shipping_query = Field()
    pre_checkout_query = Field()
    poll = Field()
    poll_answer = Field()

    def __init__(self,
                 update_id: int,
                 message: Message = None,
                 edited_message: Message = None,
                 channel_post: Message = None,
                 edited_channel_post: Message = None,
                 inline_query: InlineQuery = None,
                 chosen_inline_result: ChosenInlineResult = None,
                 callback_query: CallbackQuery = None,
                 shipping_query: ShippingQuery = None,
                 pre_checkout_query: PreCheckoutQuery = None,
                 poll: Poll = None,
                 poll_answer: PollAnswer = None
                 ):
        self.update_id = \
            Field(update_id, [int])

        self.message = \
            Field(message, [Message])

        self.edited_message = \
            Field(edited_message, [Message])

        self.channel_post = \
            Field(channel_post, [Message])

        self.edited_channel_post = \
            Field(edited_channel_post, [Message])

        self.inline_query = \
            Field(inline_query, [InlineQuery])

        self.chosen_inline_result = \
            Field(chosen_inline_result, [ChosenInlineResult])

        self.callback_query = \
            Field(callback_query, [CallbackQuery])

        self.shipping_query = \
            Field(shipping_query, [ShippingQuery])

        self.pre_checkout_query = \
            Field(pre_checkout_query, [PreCheckoutQuery])

        self.poll = \
            Field(poll, [Poll])

        self.poll_answer = \
            Field(poll_answer, [PollAnswer])
