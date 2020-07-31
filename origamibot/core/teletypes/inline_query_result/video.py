from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultVideo(InlineQueryResult):

    video_url = Field()
    mime_type = Field()
    thumb_url = Field()
    title = Field()
    caption = Field()
    parse_mode = Field()
    video_width = Field()
    video_height = Field()
    video_duration = Field()
    description = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 video_url: str,
                 mime_type: str,
                 thumb_url: str,
                 title: str,
                 caption: str = None,
                 parse_mode: str = None,
                 video_width: int = None,
                 video_height: int = None,
                 video_duration: int = None,
                 description: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'video')

        self.video_url = \
            Field(video_url, [str])

        self.mime_type = \
            Field(mime_type, [str])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.title = \
            Field(title, [str])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.video_width = \
            Field(video_width, [int])

        self.video_height = \
            Field(video_height, [int])

        self.video_duration = \
            Field(video_duration, [int])

        self.description = \
            Field(description, [str])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])
