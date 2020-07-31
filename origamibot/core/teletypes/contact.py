from .base import TelegramStructure, Field


class Contact(TelegramStructure):
    """This object represents a phone contact.

    """

    phone_number = Field()
    first_name = Field()
    last_name = Field()
    user_id = Field()
    vcard = Field()

    def __init__(self,
                 phone_number: str,
                 first_name: str,
                 last_name: str = None,
                 user_id: int = None,
                 vcard: str = None
                 ):
        self.phone_number = \
            Field(phone_number, [str])

        self.first_name = \
            Field(first_name, [str])

        self.last_name = \
            Field(last_name, [str])

        self.user_id = \
            Field(user_id, [int])

        self.vcard = \
            Field(vcard, [str])
