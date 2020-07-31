from .base import TelegramStructure, Field
from .user import User


class PollAnswer(TelegramStructure):

    poll_id = Field()
    user = Field()
    option_ids = Field()

    def __init__(self,
                 poll_id: str,
                 user: User,
                 option_ids: list
                 ):
        self.poll_id = \
            Field(poll_id, [str])

        self.user = \
            Field(user, [User])

        self.option_ids = \
            Field(option_ids, [list])
