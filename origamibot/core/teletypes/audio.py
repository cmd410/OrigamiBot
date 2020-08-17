from .base import TelegramStructure, Field
from .photo_size import PhotoSize


class Audio(TelegramStructure):
    """This object represents an audio file to be treated as music by
    the Telegram clients.

    """

    file_id = Field()
    file_unique_id = Field()
    duration = Field()
    performer = Field()
    title = Field()
    mime_type = Field()
    file_size = Field()
    thumb = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 duration: int,
                 performer: str = None,
                 title: str = None,
                 mime_type: str = None,
                 file_size: int = None,
                 thumb: PhotoSize = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.duration = \
            Field(duration, [int])

        self.performer = \
            Field(performer, [str])

        self.title = \
            Field(title, [str])

        self.mime_type = \
            Field(mime_type, [str])

        self.file_size = \
            Field(file_size, [int])
        
        self.thumb = \
            Field(thumb, [PhotoSize])
