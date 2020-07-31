from typing import List

from .base import TelegramStructure, Field, ListField
from .keyboard_button import KeyboardButton


class ReplyKeyboardMarkup(TelegramStructure):
    """This object represents a custom keyboard with reply options (see
    Introduction to bots for details and examples).

    """

    keyboard = Field()
    resize_keyboard = Field()
    one_time_keyboard = Field()
    selective = Field()

    def __init__(self,
                 keyboard: List[List[KeyboardButton]],
                 resize_keyboard: bool = None,
                 one_time_keyboard: bool = None,
                 selective: bool = None,
                 ):
        self.keyboard = \
            ListField(keyboard, [KeyboardButton])

        self.resize_keyboard = \
            Field(resize_keyboard, [bool])

        self.one_time_keyboard = \
            Field(one_time_keyboard, [bool])

        self.selective = \
            Field(selective, [bool])
