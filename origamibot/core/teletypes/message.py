from typing import List

from .base import TelegramStructure, Field, ListField
from .user import User
from .audio import Audio
from .document import Document
from .game import Game
from .sticker import Sticker
from .video import Video
from .voice import Voice
from .contact import Contact
from .location import Location
from .venue import Venue
from .message_entity import MessageEntity
from .photo_size import PhotoSize


class Message(TelegramStructure):
    """This object represents a message.

    """

    message_id = Field()
    date = Field()
    chat = Field()
    from_user = Field()
    forward_from = Field()
    forward_from_chat = Field()
    forward_from_message_id = Field()
    forward_date = Field()
    reply_to_message = Field()
    edit_date = Field()
    text = Field()
    entities = Field()
    audio = Field()
    document = Field()
    game = Field()
    photo = Field()
    sticker = Field()
    video = Field()
    voice = Field()
    caption = Field()
    contact = Field()
    location = Field()
    venue = Field()
    new_chat_member = Field()
    left_chat_member = Field()
    new_chat_title = Field()
    new_chat_photo = Field()
    delete_chat_photo = Field()
    group_chat_created = Field()
    supergroup_chat_created = Field()
    channel_chat_created = Field()
    migrate_to_chat_id = Field()
    migrate_from_chat_id = Field()
    pinned_message = Field()

    def __init__(self,
                 message_id: int,
                 date: int,
                 chat: 'Chat',
                 from_user: User = None,
                 forward_from: User = None,
                 forward_from_chat: 'Chat' = None,
                 forward_from_message_id: int = None,
                 forward_date: int = None,
                 reply_to_message: 'Message' = None,
                 edit_date: int = None,
                 text: str = None,
                 entities: List[MessageEntity] = None,
                 audio: Audio = None,
                 document: Document = None,
                 game: Game = None,
                 photo: List[PhotoSize] = None,
                 sticker: Sticker = None,
                 video: Video = None,
                 voice: Voice = None,
                 caption: str = None,
                 contact: Contact = None,
                 location: Location = None,
                 venue: Venue = None,
                 new_chat_members: User = None,
                 left_chat_member: User = None,
                 new_chat_title: str = None,
                 new_chat_photo: List[PhotoSize] = None,
                 delete_chat_photo: bool = None,
                 group_chat_created: bool = None,
                 supergroup_chat_created: bool = None,
                 channel_chat_created: bool = None,
                 migrate_to_chat_id: int = None,
                 migrate_from_chat_id: int = None,
                 pinned_message: 'Message' = None,
                 ):
        self.message_id = \
            Field(message_id, [int])

        self.date = \
            Field(date, [int])

        self.chat = \
            Field(chat, [Chat])

        self.from_user = \
            Field(from_user, [User])

        self.forward_from = \
            Field(forward_from, [User])

        self.forward_from_chat = \
            Field(forward_from_chat, [Chat])

        self.forward_from_message_id = \
            Field(forward_from_message_id, [int])

        self.forward_date = \
            Field(forward_date, [int])

        self.reply_to_message = \
            Field(reply_to_message, [Message])

        self.edit_date = \
            Field(edit_date, [int])

        self.text = \
            Field(text, [str])

        self.entities = \
            ListField(entities, [MessageEntity])

        self.audio = \
            Field(audio, [Audio])

        self.document = \
            Field(document, [Document])

        self.game = \
            Field(game, [Game])

        self.photo = \
            ListField(photo, [PhotoSize])

        self.sticker = \
            Field(sticker, [Sticker])

        self.video = \
            Field(video, [Video])

        self.voice = \
            Field(voice, [Voice])

        self.caption = \
            Field(caption, [str])

        self.contact = \
            Field(contact, [Contact])

        self.location = \
            Field(location, [Location])

        self.venue = \
            Field(venue, [Venue])

        self.new_chat_members = \
            Field(new_chat_members, [User])

        self.left_chat_member = \
            Field(left_chat_member, [User])

        self.new_chat_title = \
            Field(new_chat_title, [str])

        self.new_chat_photo = \
            ListField(new_chat_photo, [PhotoSize])

        self.delete_chat_photo = \
            Field(delete_chat_photo, [bool])

        self.group_chat_created = \
            Field(group_chat_created, [bool])

        self.supergroup_chat_created = \
            Field(supergroup_chat_created, [bool])

        self.channel_chat_created = \
            Field(channel_chat_created, [bool])

        self.migrate_to_chat_id = \
            Field(migrate_to_chat_id, [int])

        self.migrate_from_chat_id = \
            Field(migrate_from_chat_id, [int])

        self.pinned_message = \
            Field(pinned_message, [Message])


from .chat import Chat  # NOQA
