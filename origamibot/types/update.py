from ._base import TelegramObject


class Update(TelegramObject):
    update_id: int
    
    message: dict
    edited_message: dict
    
    channel_post: dict
    edited_channel_post: dict

    inline_query: dict
    chosen_inline_result: dict
    callback_query: dict
    
    shipping_query: dict
    pre_checkout_query: dict

    poll: dict
    poll_answer: dict
    
    my_chat_member: dict
    chat_member: dict
