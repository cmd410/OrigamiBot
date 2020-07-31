from .base import InputMessageContent, Field

from .location import Location
from .user import User


class ChosenInlineResult(InputMessageContent):

    result_id = Field()
    from_user = Field()
    query = Field()
    location = Field()
    inline_message_id = Field()

    def __init__(self,
                 result_id: str,
                 from_user: User,
                 query: str,
                 location: Location = None,
                 inline_message_id: str = None
                 ):
        self.result_id = \
            Field(result_id, [str])

        self.from_user = \
            Field(from_user, [User])

        self.query = \
            Field(query, [str])

        self.location = \
            Field(location, [Location])

        self.inline_message_id = \
            Field(inline_message_id, [str])
