from .base import TelegramStructure, Field


class LoginUrl(TelegramStructure):

    url = Field()
    forward_text = Field()
    bot_username = Field()
    request_write_access = Field()

    def __init__(self,
                 url: str,
                 forward_text: str = None,
                 bot_username: str = None,
                 request_write_access: bool = None
                 ):

        self.url = \
            Field(url, [str])

        self.forward_text = \
            Field(forward_text, [str])

        self.bot_username = \
            Field(bot_username, [str])

        self.request_write_access = \
            Field(request_write_access, [bool])
