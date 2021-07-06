from typing import Dict, List, Literal, Union

from yarl import URL

UpdateTypeStr = Literal[
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
    "poll",
    "poll_answer",
    "my_chat_member",
    "chat_member"
]

from .types import (
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)


ChatID = Union[str, int]

ParseMode = Literal[
    'Markdown',
    'MarkdownV2',
    'HTML'
]

URLTypes = Union[URL, str]


JSON = Union[
    None,
    int,
    float,
    bool,
    str,
    Dict[str, 'JSON'],
    List['JSON']
]


KeyboardButton = Union[str, KeyboardButton]

ReplyMarkup = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply
]
