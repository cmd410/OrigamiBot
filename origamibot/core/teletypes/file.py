from .base import TelegramStructure, Field


class File(TelegramStructure):
    """This object represents a file ready to be downloaded. The file
    can be downloaded via the link
    https://api.telegram.org/file/bot<token>/<file_path>. It is
    guaranteed that the link will be valid for at least 1 hour. When
    the link expires, a new one can be requested by calling getFile.

    """

    file_id = Field()
    file_unique_id = Field()
    file_size = Field()
    file_path = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 file_size: int = None,
                 file_path: str = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.file_size = \
            Field(file_size, [int])

        self.file_path = \
            Field(file_path, [str])
