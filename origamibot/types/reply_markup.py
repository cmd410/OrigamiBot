from typing import List, Literal, Optional

from ._base import TelegramObject


PollTypeStr = Literal['quiz', 'regular']


class KeyboardButtonPollType(TelegramObject):
    """This object represents type of a poll,
    which is allowed to be created and sent when
    the corresponding button is pressed.
    """
    type: Optional[PollTypeStr]


class KeyboardButton(TelegramObject):
    """This object represents one button of the reply keyboard.
    
    For simple text buttons String can be used instead of this
    object to specify text of the button.
    Optional fields request_contact, request_location,
    and request_poll are mutually exclusive.
    """
    text: str
    request_contact: Optional[bool]
    request_location: Optional[bool]
    request_poll: Optional[KeyboardButtonPollType]


class ReplyKeyboardMarkup(TelegramObject):
    """This object represents a custom keyboard with reply options
    """
    
    keyboard: List[List[KeyboardButton]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ReplyKeyboardRemove(TelegramObject):
    """Upon receiving a message with this object,
    Telegram clients will remove the current custom
    keyboard and display the default letter-keyboard.
    """
    
    remove_keyboard: Literal[True] = True
    selective: Optional[bool]


class CallbackGame(TelegramObject):
    """A placeholder, currently holds no information.
    """


class LoginUrl(TelegramObject):
    """This object represents a parameter of
    the inline keyboard button used to automatically
    authorize a user. 
    """
    
    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


class InlineKeyboardButton(TelegramObject):
    """This object represents one button of
    an inline keyboard. You must use exactly
    one of the optional fields.
    """
    
    text: str
    url: Optional[str]
    login_url: Optional[LoginUrl]
    callback_data: Optional[str]
    switch_inline_query: Optional[str]
    switch_inline_query_current_chat: Optional[str]
    callback_game: Optional[CallbackGame]
    pay: Optional[bool]


class InlineKeyboardMarkup(TelegramObject):
    """This object represents an inline keyboard
    that appears right next to the message it belongs to.
    """
    
    inline_keyboard: List[List[InlineKeyboardButton]]


class ForceReply(TelegramObject):
    """Upon receiving a message with this object,
    Telegram clients will display a reply interface
    to the user (act as if the user has selected the
    bot's message and tapped 'Reply').
    This can be extremely useful if you want to
    create user-friendly step-by-step interfaces
    without having to sacrifice privacy mode.
    """
    
    force_reply: Literal[True] = True
    input_field_placeholder: Optional[str]
    selective: Optional[bool]
