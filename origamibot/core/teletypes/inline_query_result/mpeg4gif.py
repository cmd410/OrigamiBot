from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultMpeg4Gif(InlineQueryResult):

    mpeg4_url = Field()
    thumb_url = Field()
    mpeg4_width = Field()
    mpeg4_height = Field()
    mpeg4_duration = Field()
    thumb_mime_type = Field()
    title = Field()
    caption = Field()
    parse_mode = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 mpeg4_url: str,
                 thumb_url: str,
                 mpeg4_width: int = None,
                 mpeg4_height: int = None,
                 mpeg4_duration: int = None,
                 thumb_mime_type: str = None,
                 title: str = None,
                 caption: str = None,
                 parse_mode: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'mpeg4_gif')

        self.mpeg4_url = \
            Field(mpeg4_url, [str])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.mpeg4_width = \
            Field(mpeg4_width, [int])

        self.mpeg4_height = \
            Field(mpeg4_height, [int])

        self.mpeg4_duration = \
            Field(mpeg4_duration, [int])

        self.thumb_mime_type = \
            Field(thumb_mime_type, [str])

        self.title = \
            Field(title, [str])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])
