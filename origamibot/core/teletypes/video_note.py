from .base import TelegramStructure, Field
from .photo_size import PhotoSize


class VideoNote(TelegramStructure):
    """This object represents a video file.

    """

    file_id = Field()
    file_unique_id = Field()
    length = Field()
    duration = Field()
    thumb = Field()
    mime_type = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 length: int,
                 duration: int,
                 thumb: PhotoSize = None,
                 file_size: int = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.length = \
            Field(length, [int])

        self.duration = \
            Field(duration, [int])

        self.thumb = \
            Field(thumb, [PhotoSize])

        self.file_size = \
            Field(file_size, [int])
