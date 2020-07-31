from .base import TelegramStructure, Field


class ReplyKeyboardRemove(TelegramStructure):
    """Upon receiving a message with this object, Telegram clients will
    remove the current custom keyboard and display the default
    letter-keyboard. By default, custom keyboards are displayed until
    a new keyboard is sent by a bot. An exception is made for one-
    time keyboards that are hidden immediately after the user presses
    a button (see ReplyKeyboardMarkup).

    """

    remove_keyboard = Field()
    selective = Field()

    def __init__(self,
                 remove_keyboard: bool,
                 selective: bool = None,
                 ):
        self.remove_keyboard = \
            Field(remove_keyboard, [bool])

        self.selective = \
            Field(selective, [bool])
