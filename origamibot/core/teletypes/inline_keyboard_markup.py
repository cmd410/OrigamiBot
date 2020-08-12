from typing import List

from .base import TelegramStructure, ListField
from .inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkup(TelegramStructure):
    """This object represents an inline keyboard that appears right next
    to the message it belongs to.

    """

    inline_keyboard = ListField()

    def __init__(self,
                 inline_keyboard: List[List[InlineKeyboardButton]],
                 ):
        self.inline_keyboard = \
            ListField(inline_keyboard, [InlineKeyboardButton])
