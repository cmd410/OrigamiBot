from .base import TelegramStructure, Field
from .encrypted_passport_element import EncryptedPassportElement
from .encrypted_credentials import EncryptedCredentials


class PassportData(TelegramStructure):

    data = Field()
    credentials = Field()

    def __init__(self,
                 data: EncryptedPassportElement,
                 credentials: EncryptedCredentials
                 ):
        self.data = \
            Field(data, [EncryptedPassportElement])

        self.credentials = \
            Field(credentials, [EncryptedCredentials])
