from flowerfield import Field, OptionalField

from ._base import TelegramType


class Audio(TelegramType):
    file_id        = Field(str)
    file_unique_id = Field(str)
    duration       = Field(int)
    performer      = OptionalField(str)
    title          = OptionalField(str)
    file_name      = OptionalField(str)
    mime_type      = OptionalField(str)
    file_size      = OptionalField(int)
    thumb          = OptionalField('PhotoSize')
