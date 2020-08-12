from .base import TelegramStructure, Field

from .location import Location
from .user import User


class InlineQuery(TelegramStructure):

    id = Field()
    from_user = Field()
    query = Field()
    offset = Field()
    location = Field()

    def __init__(self,
                 id: str,
                 from_user: User,
                 query: str,
                 offset: str,
                 location: Location = None
                 ):
        self.id = \
            Field(id, [str])

        self.from_user = \
            Field(from_user, [User])

        self.query = \
            Field(query, [str])

        self.offset = \
            Field(offset, [str])

        self.location = \
            Field(location, [Location])
