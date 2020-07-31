from .base import TelegramStructure, Field
from .photo_size import PhotoSize


class Document(TelegramStructure):
    """This object represents a general file (as opposed to photos,
    voice messages and audio files).

    """

    file_id = Field()
    file_unique_id = Field()
    thumb = Field()
    file_name = Field()
    mime_type = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 thumb: PhotoSize = None,
                 file_name: str = None,
                 mime_type: str = None,
                 file_size: int = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.thumb = \
            Field(thumb, [PhotoSize])

        self.file_name = \
            Field(file_name, [str])

        self.mime_type = \
            Field(mime_type, [str])

        self.file_size = \
            Field(file_size, [int])
