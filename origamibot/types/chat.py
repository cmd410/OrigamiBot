from typing import Optional
from ._base import TelegramObject


class Chat(TelegramObject):
    id: int
    type: str
    
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    photo: Optional[dict]
    bio: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    pinned_message: Optional['Message']
    permissions: Optional[dict]
    slow_mode_delay: Optional[int]
    message_auto_delete_time: Optional[int]
    sticker_set_name: Optional[str]
    can_set_sticker_set: Optional[bool]
    linked_chat_id: Optional[int]
    location: Optional[dict]


from .message import Message

Chat.update_forward_refs()
