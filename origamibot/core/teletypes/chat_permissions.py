from .base import Field, TelegramStructure


class ChatPermissions(TelegramStructure):

    can_send_messages = Field()
    can_send_media_messages = Field()
    can_send_polls = Field()
    can_send_other_messages = Field()
    can_add_web_page_previews = Field()
    can_change_info = Field()
    can_invite_users = Field()
    can_pin_messages = Field()

    def __init__(self,
                 can_send_messages: bool = None,
                 can_send_media_messages: bool = None,
                 can_send_polls: bool = None,
                 can_send_other_messages: bool = None,
                 can_add_web_page_previews: bool = None,
                 can_change_info: bool = None,
                 can_invite_users: bool = None,
                 can_pin_messages: bool = None
                 ):
        self.can_send_messages = \
            Field(can_send_messages, [bool])

        self.can_send_media_messages = \
            Field(can_send_media_messages, [bool])

        self.can_send_polls = \
            Field(can_send_polls, [bool])

        self.can_send_other_messages = \
            Field(can_send_other_messages, [bool])

        self.can_add_web_page_previews = \
            Field(can_add_web_page_previews, [bool])

        self.can_change_info = \
            Field(can_change_info, [bool])

        self.can_invite_users = \
            Field(can_invite_users, [bool])

        self.can_pin_messages = \
            Field(can_pin_messages, [bool])
