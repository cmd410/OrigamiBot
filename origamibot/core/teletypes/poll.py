from .base import TelegramStructure, Field, ListField
from .poll_option import PollOption
from .message_entity import MessageEntity


class Poll(TelegramStructure):

    id = Field()
    question = Field()
    options = Field()
    total_voter_count = Field()
    is_closed = Field()
    is_anonymous = Field()
    type = Field()
    allows_multiple_answers = Field()
    correct_option_id = Field()
    explanation = Field()
    explanation_entities = Field()
    open_period = Field()
    close_date = Field()

    def __init__(self,
                 id: str,
                 question: str,
                 options: list,
                 total_voter_count: int,
                 is_closed: bool,
                 is_anonymous: bool,
                 type: str,
                 allows_multiple_answers: bool,
                 correct_option_id: int = None,
                 explanation: str = None,
                 explanation_entities: list = None,
                 open_period: int = None,
                 close_date: int = None
                 ):
        self.id = \
            Field(id, [str])

        self.question = \
            Field(question, [str])

        self.options = \
            ListField(options, [PollOption])

        self.total_voter_count = \
            Field(total_voter_count, [int])

        self.is_closed = \
            Field(is_closed, [bool])

        self.is_anonymous = \
            Field(is_anonymous, [bool])

        self.type = \
            Field(type, [str])

        self.allows_multiple_answers = \
            Field(allows_multiple_answers, [bool])

        self.correct_option_id = \
            Field(correct_option_id, [int])

        self.explanation = \
            Field(explanation, [str])

        self.explanation_entities = \
            ListField(explanation_entities, [MessageEntity])

        self.open_period = \
            Field(open_period, [int])

        self.close_date = \
            Field(close_date, [int])
