from flowerfield import Field, OptionalField

from ._base import TelegramType


class PhotoSize(TelegramType):
    file_id        = Field(str)
    file_unique_id = Field(str)
    width          = Field(int)
    height         = Field(int)
    file_size      = OptionalField(int)
