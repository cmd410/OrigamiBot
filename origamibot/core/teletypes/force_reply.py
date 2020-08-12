from .base import TelegramStructure, Field


class ForceReply(TelegramStructure):
    """Upon receiving a message with this object, Telegram clients will
    display a reply interface to the user (act as if the user has
    selected the bot‘s message and tapped ’Reply'). This can be
    extremely useful if you want to create user-friendly step-by-step
    interfaces without having to sacrifice privacy mode.

    """

    force_reply = Field()
    selective = Field()

    def __init__(self,
                 force_reply: bool = True,
                 selective: bool = None,
                 ):
        self.force_reply = \
            Field(force_reply, [bool])

        self.selective = \
            Field(selective, [bool])