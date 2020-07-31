from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultGame(InlineQueryResult):

    game_short_name = Field()
    reply_markup = Field()

    def __init__(self,
                 id: str,
                 game_short_name: str,
                 reply_markup: InlineKeyboardMarkup = None
                 ):
        super().__init__(id, 'game')

        self.game_short_name = \
            Field(game_short_name, [str])

        self.reply_markup = \
            Field(reply_markup, [InputMessageContent])
