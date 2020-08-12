from .base import TelegramStructure, Field
from .login_url import LoginUrl


class InlineKeyboardButton(TelegramStructure):

    text = Field()
    url = Field()
    login_url = Field()
    callback_data = Field()
    switch_inline_query = Field()
    switch_inline_query_current_chat = Field()
    callback_game = Field()
    pay = Field()

    def __init__(self,
                 text: str,
                 url: str = None,
                 login_url: LoginUrl = None,
                 callback_data: str = None,
                 switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None,
                 callback_game: dict = None,
                 pay: bool = None
                 ):
        self.text = \
            Field(text, [str])

        self.url = \
            Field(url, [str])

        self.login_url = \
            Field(login_url, [LoginUrl])

        self.callback_data = \
            Field(callback_data, [str])

        self.switch_inline_query = \
            Field(switch_inline_query, [str])

        self.switch_inline_query_current_chat = \
            Field(switch_inline_query_current_chat, [str])

        # NOTE callback game is a "placeholder" type
        # that does not contain any info
        self.callback_game = \
            Field()

        self.pay = \
            Field(pay, [bool])
