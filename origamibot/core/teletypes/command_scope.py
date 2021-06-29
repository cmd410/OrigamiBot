from typing import Union
from .base import TelegramStructure, Field


class BotCommandScope(TelegramStructure):
    type: str = Field()
    
    
    def __init__(self, type: str) -> None:
        self.type = \
            Field(type, [str])


class BotCommandScopeDefault(BotCommandScope):
    def __init__(self) -> None:
        super().__init__('default')
        

class BotCommandScopeAllPrivateChats(BotCommandScope):
    def __init__(self) -> None:
        super().__init__('all_private_chats')


class BotCommandScopeAllGroupChats(BotCommandScope):
    def __init__(self) -> None:
        super().__init__('all_group_chats')


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    def __init__(self) -> None:
        super().__init__('all_chat_administrators')


class BotCommandScopeChat(BotCommandScope):
    
    chat_id: Union[int, str] = Field()
    
    def __init__(self, chat_id: Union[int, str]) -> None:
        self.chat_id = Field(chat_id, [int])
        super().__init__('chat')


class BotCommandScopeChatAdministrators(BotCommandScope):
    
    chat_id: Union[int, str] = Field()
    
    def __init__(self, chat_id: Union[int, str]) -> None:
        self.chat_id = Field(chat_id, [int])
        super().__init__('chat_administrators')


class BotCommandScopeChatMember(BotCommandScope):
    
    chat_id: Union[int, str] = Field()
    
    def __init__(self, chat_id: Union[int, str]) -> None:
        self.chat_id = Field(chat_id, [int])
        super().__init__('chat_member')

