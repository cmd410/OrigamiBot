from .base import TelegramStructure, Field


class EncryptedCredentials(TelegramStructure):

    data = Field()
    hash = Field()
    secret = Field()

    def __init__(self,
                 data: str,
                 hash: str,
                 secret: str
                 ):

        self.data = \
            Field(data, [str])

        self.hash = \
            Field(hash, [str])

        self.secret = \
            Field(secret, [str])
