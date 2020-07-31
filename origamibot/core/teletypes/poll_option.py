from .base import TelegramStructure, Field


class PollOption(TelegramStructure):

    text = Field()
    voter_count = Field()

    def __init__(self,
                 text: str,
                 voter_count: int
                 ):
        self.text = \
            Field(text, [str])

        self.voter_count = \
            Field(voter_count, [int])
