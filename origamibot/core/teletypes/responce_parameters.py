from .base import Field, TelegramStructure


class ResponseParameters(TelegramStructure):

    migrate_to_chat_id = Field()
    retry_after = Field()

    def __init__(self,
                 migrate_to_chat_id: int = None,
                 retry_after: int = None
                 ):

        self.migrate_to_chat_id = \
            Field(migrate_to_chat_id, [int])

        self.retry_after = \
            Field(retry_after, [int])
