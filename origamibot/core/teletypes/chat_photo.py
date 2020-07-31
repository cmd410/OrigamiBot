from .base import Field, TelegramStructure


class ChatPhoto(TelegramStructure):

    small_file_id = Field()
    small_file_unique_id = Field()
    big_file_id = Field()
    big_file_unique_id = Field()

    def __init__(self,
                 small_file_id: str,
                 small_file_unique_id: str,
                 big_file_id: str,
                 big_file_unique_id: str,
                 ):

        self.small_file_id = \
            Field(small_file_id, [str])

        self.small_file_unique_id = \
            Field(small_file_unique_id, [str])

        self.big_file_id = \
            Field(big_file_id, [str])

        self.big_file_unique_id = \
            Field(big_file_unique_id, [str])
