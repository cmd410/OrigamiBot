from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultLocation(InlineQueryResult):

    latitude = Field()
    longitude = Field()
    title = Field()
    live_period = Field()
    reply_markup = Field()
    input_message_content = Field()
    thumb_url = Field()
    thumb_width = Field()
    thumb_height = Field()

    def __init__(self,
                 id: str,
                 latitude: float,
                 longitude: float,
                 title: str,
                 live_period: int = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None,
                 thumb_width: int = None,
                 thumb_height: int = None
                 ):
        super().__init__(id, 'location')

        self.latitude = \
            Field(latitude, [float])

        self.longitude = \
            Field(longitude, [float])

        self.title = \
            Field(title, [str])

        self.live_period = \
            Field(live_period, [int])

        self.reply_markup = \
            Field(reply_markup, [str])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.thumb_width = \
            Field(thumb_width, [int])

        self.thumb_height = \
            Field(thumb_height, [int])
