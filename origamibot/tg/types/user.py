from flowerfield import Field, OptionalField

from ._base import TelegramType


class User(TelegramType):
    # Required fields
    id         = Field(int)
    is_bot     = Field(bool)
    first_name = Field(str)

    # Optional
    first_name                  = OptionalField(str)
    last_name                   = OptionalField(str)
    username                    = OptionalField(str)
    language_code               = OptionalField(str)
    can_join_groups             = OptionalField(bool)
    can_read_all_group_messages = OptionalField(bool)
    supports_inline_queries     = OptionalField(bool)
