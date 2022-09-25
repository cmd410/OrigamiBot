from typing import Optional
from ._base import TelegramObject
from .message import Message


class Update(TelegramObject):
    update_id: int

    message: Optional[Message]
    edited_message: Optional[Message]

    channel_post: Optional[Message]
    edited_channel_post: Optional[Message]

    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]

    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]

    poll: Optional[dict]
    poll_answer: Optional[dict]

    my_chat_member: Optional[dict]
    chat_member: Optional[dict]
