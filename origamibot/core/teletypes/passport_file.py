from .base import TelegramStructure, Field


class PassportFile(TelegramStructure):

    file_id = Field()
    file_unique_id = Field()
    file_size = Field()
    file_date = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 file_size: int,
                 file_date: int
                 ):

        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.file_size = \
            Field(file_size, [int])

        self.file_date = \
            Field(file_date, [int])
