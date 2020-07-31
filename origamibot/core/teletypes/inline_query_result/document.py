from ..base import InlineQueryResult, Field, InputMessageContent

from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultDocument(InlineQueryResult):

    title = Field()
    document_url = Field()
    mime_type = Field()
    caption = Field()
    parse_mode = Field()
    description = Field()
    reply_markup = Field()
    input_message_content = Field()
    thumb_url = Field()
    thumb_width = Field()
    thumb_height = Field()

    def __init__(self,
                 id: str,
                 title: str,
                 document_url: str,
                 mime_type: str,
                 caption: str = None,
                 parse_mode: str = None,
                 description: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None,
                 thumb_width: int = None,
                 thumb_height: int = None
                 ):
        super().__init__(id, 'document')

        self.title = \
            Field(title, [str])

        self.document_url = \
            Field(document_url, [str])

        self.mime_type = \
            Field(mime_type, [str])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.description = \
            Field(description, [str])

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
