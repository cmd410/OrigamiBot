from .base import TelegramStructure, Field


class Voice(TelegramStructure):
    """This object represents a voice note.

    """

    file_id = Field()
    file_unique_id = Field()
    duration = Field()
    mime_type = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 duration: int,
                 mime_type: str = None,
                 file_size: int = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.duration = \
            Field(duration, [int])

        self.mime_type = \
            Field(mime_type, [str])

        self.file_size = \
            Field(file_size, [int])
