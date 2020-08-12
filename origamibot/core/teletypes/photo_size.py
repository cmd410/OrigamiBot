from .base import TelegramStructure, Field


class PhotoSize(TelegramStructure):
    """This object represents one size of a photo or a file / sticker
    thumbnail.

    """

    file_id = Field()
    file_unique_id = Field()
    width = Field()
    height = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 width: int,
                 height: int,
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

        self.file_size = \
            Field(file_size, [int])
