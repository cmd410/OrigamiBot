from .base import TelegramStructure, Field
from .user import User


class MessageEntity(TelegramStructure):
    """This object represents one special entity in a text message. For
    example, hashtags, usernames, URLs, etc.

    """

    type = Field()
    offset = Field()
    length = Field()
    url = Field()
    user = Field()
    language = Field()

    def __init__(self,
                 type: str,
                 offset: int,
                 length: int,
                 url: str = None,
                 user: User = None,
                 language: str = None
                 ):
        self.type = \
            Field(type, [str])

        self.offset = \
            Field(offset, [int])

        self.length = \
            Field(length, [int])

        self.url = \
            Field(url, [str])

        self.user = \
            Field(user, [User])
        
        self.language = \
            Field(language, [str])
