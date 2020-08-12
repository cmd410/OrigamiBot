from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultAudio(InlineQueryResult):

    audio_url = Field()
    title = Field()
    caption = Field()
    parse_mode = Field()
    performer = Field()
    audio_duration = Field()
    reply_markup = Field()
    input_message_content = Field()

    def __init__(self,
                 id: str,
                 audio_url: str,
                 title: str,
                 caption: str = None,
                 parse_mode: str = None,
                 performer: str = None,
                 audio_duration: int = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None
                 ):
        super().__init__(id, 'audio')

        self.audio_url = \
            Field(audio_url, [str])

        self.title = \
            Field(title, [str])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.performer = \
            Field(performer, [str])

        self.audio_duration = \
            Field(audio_duration, [int])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])
