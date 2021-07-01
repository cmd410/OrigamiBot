from ._base import TelegramObject
from .message import Message


class Update(TelegramObject):
    update_id: int
    
    message: Message
    edited_message: Message
    
    channel_post: Message
    edited_channel_post: Message

    inline_query: dict
    chosen_inline_result: dict
    callback_query: dict
    
    shipping_query: dict
    pre_checkout_query: dict

    poll: dict
    poll_answer: dict
    
    my_chat_member: dict
    chat_member: dict
