from .base import TelegramStructure, Field, ListField
from .passport_file import PassportFile


class EncryptedPassportElement(TelegramStructure):

    type = Field()
    data = Field()
    hash = Field()
    phone_number = Field()
    email = Field()
    files = Field()
    front_side = Field()
    reverse_side = Field()
    selfie = Field()
    translation = Field()

    def __init__(self,
                 type: str,
                 data: str,
                 hash: str,
                 phone_number: str = None,
                 email: str = None,
                 files: list = None,
                 front_side: PassportFile = None,
                 reverse_side: PassportFile = None,
                 selfie: PassportFile = None,
                 translation: PassportFile = None
                 ):
        self.type = \
            Field(type, [str])

        self.data = \
            Field(data, [str])

        self.hash = \
            Field(hash, [str])

        self.phone_number = \
            Field(phone_number, [str])

        self.email = \
            Field(email, [str])

        self.files = \
            ListField(files, [PassportFile])

        self.front_side = \
            Field(front_side, [PassportFile])

        self.reverse_side = \
            Field(reverse_side, [PassportFile])

        self.selfie = \
            Field(reverse_side, [PassportFile])

        self.translation = \
            Field(translation, [PassportFile])
