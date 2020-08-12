from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultGif(InlineQueryResult):

    gif_url = Field()
    thumb_url = Field()
    gif_width = Field()
    gif_height = Field()
    gif_duration = Field()
    thumb_mime_type = Field()
    title = Field()
    caption = Field()
    parse_mode = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 gif_url: str,
                 thumb_url: str,
                 gif_width: int = None,
                 gif_height: int = None,
                 gif_duration: int = None,
                 thumb_mime_type: str = None,
                 title: str = None,
                 caption: str = None,
                 parse_mode: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'gif')

        self.gif_url = \
            Field(gif_url, [str])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.gif_width = \
            Field(gif_width, [int])

        self.gif_height = \
            Field(gif_height, [int])

        self.gif_duration = \
            Field(gif_duration, [int])

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
