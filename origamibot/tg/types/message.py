from typing import Optional, List

from flowerfield import Field, ListField, OptionalField

from ._base import TelegramType
from .inline_keyboard import InlineKeyboardMarkup


class Message(TelegramType):
    # bot that posseses message

    # Required fields
    message_id = Field(int)
    date       = Field(int)
    chat       = Field("Chat")

    # Optional
    from_user              = OptionalField("User", alias="from")
    sender_chat            = OptionalField("Chat")
    forward_from           = OptionalField("User")
    forward_from_chat      = OptionalField("Chat")
    forward_from_signature = OptionalField(str)
    forward_date           = OptionalField(int)
    reply_to_message       = OptionalField("Message")
    via_bot                = OptionalField("User")
    edit_date              = OptionalField(int)
    media_group_id         = OptionalField(str)
    author_signature       = OptionalField(str)
    text                   = OptionalField(str)
    entities               = ListField("MessageEntity")
    animation              = OptionalField("Animation")
    audio                  = OptionalField("Audio")
    document               = OptionalField("Document")
    photo                  = ListField("PhotoSize")
    sticker                = OptionalField("Sticker")
    reply_markup           = OptionalField("ReplyMarkup")
    # TODO fields:
    # video
    # video_note
    # voice
    # caption
    # caption_entities
    # contact
    # dice
    # game
    # poll
    # venue
    # location
    # new_chat_members
    # left_chat_member
    # new_chat_title
    # new_chat_photo
    # delete_chat_photo
    # group_chat_created
    # supergroup_chat_created
    # channel_chat_created
    # migrate_to_chat_id
    # migrate_from_chat_id
    # pinned_message
    # invoice
    # successful_payment
    # connected_website
    # passport_data
    # proximity_alert_triggered

    def edit_text(self,
                  text: str,
                  parse_mode: Optional[str] = None,
                  disable_web_page_preview: Optional[bool] = None,
                  reply_markup: Optional[InlineKeyboardMarkup] = None
                  ) -> "Message":
        """Change text of current message
        """
        assert self._bot is not None
        return self._bot.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )

    def reply(self,
              text: str,
              parse_mode: Optional[str] = None,
              enities: Optional[List] = None,
              disable_web_page_preview: Optional[bool] = None,
              disable_notification: Optional[bool] = None,
              allow_sending_without_reply: Optional[bool] = None,
              reply_markup: Optional = None
              ) -> "Message":
        """Send a reply to this message
        """
        assert self._bot is not None
        return self._bot.send_message(
            chat_id=self.chat.id,
            reply_to_message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            enities=enities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
