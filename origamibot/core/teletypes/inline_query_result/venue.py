from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultVenue(InlineQueryResult):

    latitude = Field()
    longitude = Field()
    title = Field()
    address = Field()
    foursquare_id = Field()
    foursquare_type = Field()
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
                 address: str,
                 foursquare_id: str = None,
                 foursquare_type: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None,
                 thumb_width: int = None,
                 thumb_height: int = None
                 ):
        super().__init__(id, 'venue')

        self.latitude = \
            Field(latitude, [float])

        self.longitude = \
            Field(longitude, [longitude])

        self.title = \
            Field(title, [str])

        self.address = \
            Field(address, [str])

        self.foursquare_id = \
            Field(foursquare_id, [str])

        self.foursquare_type = \
            Field(foursquare_type, [str])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.thumb_width = \
            Field(thumb_width, [int])

        self.thumb_height = \
            Field(thumb_height, [int])
