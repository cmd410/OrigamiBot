from .base import TelegramStructure, Field


class User(TelegramStructure):
    """This object represents a Telegram user or bot.
    """

    id = Field()
    is_bot = Field()
    first_name = Field()
    last_name = Field()
    username = Field()
    language_code = Field()
    can_join_groups = Field()
    can_read_all_group_messages = Field()
    supports_inline_queries = Field()
    is_premium = Field()

    def __init__(self,
                 id: int,
                 is_bot: bool,
                 first_name: str,
                 last_name: str = None,
                 username: str = None,
                 language_code: str = None,
                 can_join_groups: bool = None,
                 can_read_all_group_messages: bool = None,
                 supports_inline_queries: bool = None,
                 is_premium: bool = False
                 ):
        self.id = \
            Field(id, [int])

        self.is_bot = \
            Field(is_bot, [bool])

        self.first_name = \
            Field(first_name, [str])

        self.last_name = \
            Field(last_name, [str])

        self.username = \
            Field(username, [str])

        self.language_code = \
            Field(language_code, [str])

        self.can_join_groups = \
            Field(can_join_groups, [bool])

        self.can_read_all_group_messages = \
            Field(can_read_all_group_messages, [bool])

        self.supports_inline_queries = \
            Field(supports_inline_queries, [bool])
        
        self.is_premium = \
            Field(is_premium, [bool])
