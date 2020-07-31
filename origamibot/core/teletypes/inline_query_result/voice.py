from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultVoice(InlineQueryResult):

    voice_url = Field()
    title = Field()
    caption = Field()
    parse_mode = Field()
    voice_duration = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 voice_url: str,
                 title: str,
                 caption: str = None,
                 parse_mode: str = None,
                 voice_duration: int = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'voice')

        self.voice_url = \
            Field(voice_url, [str])

        self.title = \
            Field(title, [str])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.voice_duration = \
            Field(voice_duration, [int])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])
