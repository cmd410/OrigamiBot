from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultArticle(InlineQueryResult):

    title = Field()
    input_message_content = Field()
    reply_markup = Field()
    url = Field()
    hide_url = Field()
    description = Field()
    thumb_url = Field()
    thumb_width = Field()
    thumb_height = Field()

    def __init__(self,
                 id: str,
                 title: str,
                 input_message_content: InputMessageContent,
                 reply_markup: InlineKeyboardMarkup = None,
                 url: str = None,
                 hide_url: bool = None,
                 description: str = None,
                 thumb_url: str = None,
                 thumb_width: int = None,
                 thumb_height: int = None
                 ):
        super().__init__(id, 'article')

        self.title = \
            Field(title, [str])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.url = \
            Field(url, [str])

        self.hide_url = \
            Field(hide_url, [bool])

        self.description = \
            Field(description, [str])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.thumb_width = \
            Field(thumb_width, [int])

        self.thumb_height = \
            Field(thumb_height, [int])
