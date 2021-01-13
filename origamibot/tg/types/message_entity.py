from flowerfield import Field, OptionalField

from ._base import TelegramType


class MessageEntity(TelegramType):
    type   = Field(str)
    offset = Field(int)
    length = Field(int)
    
    url      = OptionalField(str)
    user     = OptionalField('User')
    language = OptionalField(str)
