from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultPhoto(InlineQueryResult):

    photo_url = Field()
    thumb_url = Field()
    photo_width = Field()
    title = Field()
    description = Field()
    caption = Field()
    parse_mode = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 photo_url: str,
                 thumb_url: str,
                 photo_width: int = None,
                 title: str = None,
                 description: str = None,
                 caption: str = None,
                 parse_mode: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'photo')

        self.photo_url = \
            Field(photo_url, [str])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.photo_width = \
            Field(photo_width, [int])

        self.title = \
            Field(title, [str])

        self.description = \
            Field(description, [str])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])
