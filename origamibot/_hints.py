from typing import Dict, List, Literal, Union

from yarl import URL


URLTypes = Union[URL, str]


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


JSON = Union[
    None,
    int,
    float,
    bool,
    str,
    Dict[str, 'JSON'],
    List['JSON']
]
