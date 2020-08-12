from .base import Field, TelegramStructure
from .user import User


class ChatMember(TelegramStructure):

    user = Field()
    status = Field()
    custom_title = Field()
    until_date = Field()
    can_be_edited = Field()
    can_post_messages = Field()
    can_edit_messages = Field()
    can_delete_messages = Field()
    can_restrict_members = Field()
    can_promote_members = Field()
    can_change_info = Field()
    can_invite_users = Field()
    can_pin_messages = Field()
    is_member = Field()
    can_send_messages = Field()
    can_send_media_messages = Field()
    can_send_polls = Field()
    can_send_other_messages = Field()
    can_add_web_page_previews = Field()

    def __init__(self,
                 user: User,
                 status: str,
                 custom_title: str = None,
                 until_date: int = None,
                 can_be_edited: bool = None,
                 can_post_messages: bool = None,
                 can_edit_messages: bool = None,
                 can_delete_messages: bool = None,
                 can_restrict_members: bool = None,
                 can_promote_members: bool = None,
                 can_change_info: bool = None,
                 can_invite_users: bool = None,
                 can_pin_messages: bool = None,
                 is_member: bool = None,
                 can_send_messages: bool = None,
                 can_send_media_messages: bool = None,
                 can_send_polls: bool = None,
                 can_send_other_messages: bool = None,
                 can_add_web_page_previews: bool = None
                 ):
        self.user = \
            Field(user, [User])

        self.status = \
            Field(status, [str])

        self.custom_title = \
            Field(custom_title, [str])

        self.until_date = \
            Field(until_date, [int])

        self.can_be_edited = \
            Field(can_be_edited, [bool])

        self.can_post_messages = \
            Field(can_post_messages, [bool])

        self.can_edit_messages = \
            Field(can_edit_messages, [bool])

        self.can_delete_messages = \
            Field(can_delete_messages, [bool])

        self.can_restrict_members = \
            Field(can_restrict_members, [bool])

        self.can_promote_members = \
            Field(can_promote_members, [bool])

        self.can_change_info = \
            Field(can_change_info, [bool])

        self.can_invite_users = \
            Field(can_invite_users, [bool])

        self.can_pin_messages = \
            Field(can_pin_messages, [bool])

        self.is_member = \
            Field(is_member, [bool])

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
