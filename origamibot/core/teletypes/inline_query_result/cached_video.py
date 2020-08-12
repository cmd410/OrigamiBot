from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultCachedVideo(InlineQueryResult):

    video_file_id = Field()
    title = Field()
    description = Field()
    caption = Field()
    parse_mode = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 video_file_id: str,
                 title: str,
                 description: str = None,
                 caption: str = None,
                 parse_mode: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'video')

        self.video_file_id = \
            Field(video_file_id, [str])

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
