from flowerfield import Field

from ._base import TelegramType


class ChatPhoto(TelegramType):
    small_file_id        = Field(str)
    small_file_unique_id = Field(str)
    big_file_id          = Field(str)
    big_file_unique_id   = Field(str)