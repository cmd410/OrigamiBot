from typing import List, Literal, Optional

from pydantic.fields import Field

from ._base import TelegramObject
from .user import User


class Message(TelegramObject):
    """This object represents a message.
    """
    
    message_id: int
    
    from_user: Optional[User] = Field(alias='from')
    sender_chat: Optional[dict]
    date: Optional[int]
    
    forward_from: Optional[User]
    forward_from_chat: Optional[dict]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    
    reply_to_message: Optional['Message']
    via_bot: Optional[User]
    edit_date: Optional[int]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    text: Optional[str]
    entities: Optional[List[dict]]
    
    animation: Optional[dict]
    audio: Optional[dict]
    document: Optional[dict]
    photo: Optional[List[dict]]
    sticker: Optional[dict]
    video: Optional[dict]
    video_note: Optional[dict]
    voice: Optional[dict]
    
    caption: Optional[dict]
    caption_entities: Optional[List[dict]]
    
    contact: Optional[dict]
    dice: Optional[dict]
    game: Optional[dict]
    poll: Optional[dict]
    venue: Optional[dict]
    location: Optional[dict]
    
    new_chat_members: Optional[List[User]]
    left_chat_member: Optional[User]
    
    new_chat_title: Optional[str]
    new_chat_photo: Optional[List[dict]]
    delete_chat_photo: Optional[Literal[True]]
    group_chat_created: Optional[Literal[True]]
    supergroup_chat_created: Optional[Literal[True]]
    channel_chat_created: Optional[Literal[True]]
    
    message_auto_delete_timer_changed: Optional[dict]
    
    migrate_to_chat_id: Optional[int]
    migrate_from_chat_id: Optional[int]
    
    pinned_message: Optional[dict]
    
    invoice: Optional[dict]
    successful_payment: Optional[dict]
    
    connected_website: Optional[dict]
    
    passport_data: Optional[dict]
    proximity_alert_triggered: Optional[dict]
    
    voice_chat_scheduled: Optional[dict]
    voice_chat_started: Optional[dict]
    voice_chat_ended: Optional[dict]
    voice_chat_participants_invited: Optional[dict]
    
    reply_markup: Optional[dict]
    