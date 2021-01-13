from flowerfield import Field, OptionalField

from ._base import TelegramType


class Chat(TelegramType):
    # Required
    id   = Field(int)
    type = Field(str)
    
    # Optional
    title               = OptionalField(str)
    username            = OptionalField(str)
    first_name          = OptionalField(str)
    last_name           = OptionalField(str)
    photo               = OptionalField('ChatPhoto')
    bio                 = OptionalField(str)
    description         = OptionalField(str)
    invite_link         = OptionalField(str)
    pinned_message      = OptionalField('Message')
    permissions         = OptionalField('ChatPermissions')
    slow_mode_delay     = OptionalField(int)
    sticker_set_name    = OptionalField(str)
    can_set_sticker_set = OptionalField(bool)
    linked_chat_id      = OptionalField(int)
    location            = OptionalField('ChatLocation')
