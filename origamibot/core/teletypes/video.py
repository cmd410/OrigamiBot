from .base import TelegramStructure, Field
from .photo_size import PhotoSize


class Video(TelegramStructure):
    """This object represents a video file.

    """

    file_id = Field()
    file_unique_id = Field()
    file_name = Field()
    width = Field()
    height = Field()
    duration = Field()
    thumb = Field()
    mime_type = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 width: int,
                 height: int,
                 duration: int,
                 thumb: PhotoSize = None,
                 mime_type: str = None,
                 file_size: int = None,
                 file_name: str = None
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.file_name = \
            Field(file_name, [str])

        self.width = \
            Field(width, [int])

        self.height = \
            Field(height, [int])

        self.duration = \
            Field(duration, [int])

        self.thumb = \
            Field(thumb, [PhotoSize])

        self.mime_type = \
            Field(mime_type, [str])

        self.file_size = \
            Field(file_size, [int])
