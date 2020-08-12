from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultContact(InlineQueryResult):

    phone_number = Field()
    first_name = Field()
    last_name = Field()
    vcard = Field()
    reply_markup = Field()
    input_message_content = Field()
    thumb_url = Field()
    thumb_width = Field()
    thumb_height = Field()

    def __init__(self,
                 id: str,
                 phone_number: str,
                 first_name: str,
                 last_name: str = None,
                 vcard: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None,
                 thumb_width: int = None,
                 thumb_height: int = None
                 ):
        super().__init__(id, 'contact')

        self.phone_number = \
            Field(phone_number, [str])

        self.first_name = \
            Field(first_name, [str])

        self.last_name = \
            Field(last_name, [str])

        self.vcard = \
            Field(vcard, [str])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])

        self.input_message_content = \
            Field(input_message_content, [InputMessageContent])

        self.thumb_url = \
            Field(thumb_url, [str])

        self.thumb_width = \
            Field(thumb_width, [str])

        self.thumb_height = \
            Field(thumb_height, [str])
