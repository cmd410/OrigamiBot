from .base import InputMessageContent, Field


class InputTextMessageContent(InputMessageContent):

    message_text = Field()
    parse_mode = Field()
    disable_web_page_preview = Field()

    def __init__(self,
                 message_text: str,
                 parse_mode: str = None,
                 disable_web_page_preview: bool = None
                 ):
        self.message_text = \
            Field(message_text, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.disable_web_page_preview = \
            Field(disable_web_page_preview, [bool])
