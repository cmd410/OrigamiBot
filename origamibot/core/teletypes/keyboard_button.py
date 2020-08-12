from .base import TelegramStructure, Field


class KeyboardButton(TelegramStructure):
    """This object represents one button of the reply keyboard. For
    simple text buttons String can be used instead of this object to
    specify text of the button. Optional fields are mutually
    exclusive.

    """

    text = Field()
    request_contact = Field()
    request_location = Field()

    def __init__(self,
                 text: str,
                 request_contact: bool = None,
                 request_location: bool = None,
                 ):
        self.text = \
            Field(text, [str])

        self.request_contact = \
            Field(request_contact, [bool])

        self.request_location = \
            Field(request_location, [bool])
