from flowerfield import Field, OptionalField

from ._base import TelegramType


class Animation(TelegramType):
    file_id        = Field(str)
    file_unique_id = Field(str)
    width          = Field(int)
    height         = Field(int)
    duration       = Field(int)

    thumb     = OptionalField("PhotoSize")
    file_name = OptionalField(str)
    mime_type = OptionalField(str)
    file_size = OptionalField(int)
