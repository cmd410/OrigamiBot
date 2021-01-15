from typing import Optional

from flowerfield import Field, ListField, OptionalField

from ._base import TelegramType


class LoginUrl(TelegramType):
    url = Field(str)

    forward_text         = OptionalField(str)
    bot_username         = OptionalField(str)
    request_write_access = OptionalField(bool)


class InlineKeyboardButton(TelegramType):
    text = Field(str)

    url                              = OptionalField(str)
    login_url                        = OptionalField(LoginUrl)
    callback_data                    = OptionalField(str)
    switch_inline_query              = OptionalField(str)
    switch_inline_query_current_chat = OptionalField(str)
    pay                              = OptionalField(bool)


class InlineKeyboardMarkup(TelegramType):
    inline_keyboard = ListField(InlineKeyboardButton)

    def add_row(self):
        if not self.inline_keyboard:
            self.inline_keyboard = [[]]
        else:
            self.inline_keyboard.append([])

    def add_button(self,
                   text: str,
                   url: Optional[str] = None,
                   login_url: Optional[LoginUrl] = None,
                   switch_inline_query: Optional[str] = None,
                   switch_inline_query_current_chat: Optional[str] = None,
                   pay: Optional[bool] = None,
                   ) -> InlineKeyboardButton:
        button = InlineKeyboardButton.from_dict(locals())

        if not self.inline_keyboard:
            self.add_row()

        self.inline_keyboard[-1].append(button)

        return button
