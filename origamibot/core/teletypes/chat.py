from .base import Field, TelegramStructure

from .chat_photo import ChatPhoto
from .chat_permissions import ChatPermissions


class Chat(TelegramStructure):

    id = Field()
    type = Field()
    title = Field()
    username = Field()
    first_name = Field()
    last_name = Field()
    chat_photo = Field()
    description = Field()
    invite_link = Field()
    pinned_message = Field()
    permissions = Field()
    slow_mode_delay = Field()
    sticker_set_name = Field()
    can_set_sticker_set = Field()
    all_members_are_administrators = Field()

    def __init__(self,
                 id: int,
                 type: str,
                 title: str = None,
                 username: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 chat_photo: ChatPhoto = None,
                 description: str = None,
                 invite_link: str = None,
                 pinned_message: 'Message' = None,
                 permissions: ChatPermissions = None,
                 slow_mode_delay: int = None,
                 sticker_set_name: str = None,
                 can_set_sticker_set: bool = None,
                 all_members_are_administrators: bool = None
                 ):
        self.id = \
            Field(id, [int])

        self.type = \
            Field(type, [str])

        self.title = \
            Field(title, [str])

        self.username = \
            Field(username, [str])

        self.first_name = \
            Field(first_name, [str])

        self.last_name = \
            Field(last_name, [str])

        self.chat_photo = \
            Field(chat_photo, [ChatPhoto])

        self.description = \
            Field(description, [str])

        self.invite_link = \
            Field(invite_link, [str])

        self.pinned_message = \
            Field(pinned_message, [Message])

        self.permissions = \
            Field(permissions, [ChatPermissions])

        self.slow_mode_delay = \
            Field(slow_mode_delay, [int])

        self.sticker_set_name = \
            Field(sticker_set_name, [str])

        self.can_set_sticker_set = \
            Field(can_set_sticker_set, [bool])

        self.all_members_are_administrators = \
            Field(all_members_are_administrators, [bool])


from .message import Message  # NOQA
