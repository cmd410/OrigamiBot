from .base import InputMessageContent, Field


class InputContactMessageContent(InputMessageContent):

    phone_number = Field()
    first_name = Field()
    last_name = Field()
    vcard = Field()

    def __init__(self,
                 phone_number: str,
                 first_name: str,
                 last_name: str = None,
                 vcard: str = None
                 ):
        self.phone_number = \
            Field(phone_number, [str])

        self.first_name = \
            Field(first_name, [str])

        self.last_name = \
            Field(last_name, [str])

        self.vcard = \
            Field(vcard, [str])
