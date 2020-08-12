from .base import Field, TelegramStructure
from .message import Message
from .user import User


class CallbackQuery(TelegramStructure):

    id = Field()
    from_user = Field()
    chat_instance = Field()
    message = Field()
    inline_message_id = Field()
    data = Field()
    game_short_name = Field()

    def __init__(self,
                 id: str,
                 from_user: User,
                 chat_instance: str,
                 message: Message = None,
                 inline_message_id: str = None,
                 data: str = None,
                 game_short_name: str = None
                 ):
        self.id = \
            Field(id, [str])

        self.from_user = \
            Field(from_user, [User])

        self.chat_instance = \
            Field(chat_instance, [str])

        self.message = \
            Field(message, [Message])

        self.inline_message_id = \
            Field(inline_message_id, [str])

        self.data = \
            Field(data, [str])

        self.game_short_name = \
            Field(game_short_name, [str])
