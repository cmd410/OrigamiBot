from .base import Field, TelegramStructure


class BotCommand(TelegramStructure):

    command = Field()
    description = Field()

    def __init__(self,
                 command: str = None,
                 description: str = None
                 ):

        self.command = \
            Field(command, [str])

        self.description = \
            Field(description, [str])
