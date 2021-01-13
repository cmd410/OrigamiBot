from flowerfield import Field, ListField, OptionalField

from ._base import TelegramType


class Message(TelegramType):
    # Required fields
    message_id = Field(int)
    date       = Field(int)
    chat       = Field('Chat')
    
    # Optional
    from_user              = OptionalField('User', alias='from')
    sender_chat            = OptionalField('Chat')
    forward_from           = OptionalField('User')
    forward_from_chat      = OptionalField('Chat')
    forward_from_signature = OptionalField(str)
    forward_date           = OptionalField(int)
    reply_to_message       = OptionalField('Message')
    via_bot                = OptionalField('User')
    edit_date              = OptionalField(int)
    media_group_id         = OptionalField(str)
    author_signature       = OptionalField(str)
    text                   = OptionalField(str)
    entities               = ListField('MessageEntity')
    animation              = OptionalField('Animation')
    audio                  = OptionalField('Audio')
    document               = OptionalField('Document')
    photo                  = ListField('PhotoSize')
    sticker                = OptionalField('Sticker')
    reply_markup           = OptionalField('ReplyMarkup')
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
