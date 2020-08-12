from .base import TelegramStructure, Field
from .photo_size import PhotoSize
from .mask_position import MaskPosition


class Sticker(TelegramStructure):
    """This object represents a sticker.

    """

    file_id = Field()
    file_unique_id = Field()
    width = Field()
    height = Field()
    is_animated = Field()
    thumb = Field()
    emoji = Field()
    set_name = Field()
    mask_position = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 width: int,
                 height: int,
                 is_animated: bool,
                 thumb: PhotoSize = None,
                 emoji: str = None,
                 set_name: str = None,
                 mask_position: MaskPosition = None,
                 file_size: int = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.width = \
            Field(width, [int])

        self.height = \
            Field(height, [int])

        self.is_animated = \
            Field(is_animated, [bool])

        self.thumb = \
            Field(thumb, [PhotoSize])

        self.emoji = \
            Field(emoji, [str])

        self.set_name = \
            Field(set_name, [str])

        self.mask_position = \
            Field(mask_position, [MaskPosition])

        self.file_size = \
            Field(file_size, [int])
