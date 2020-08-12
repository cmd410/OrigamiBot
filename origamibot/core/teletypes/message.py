from typing import List

from .base import TelegramStructure, Field, ListField
from .user import User
from .audio import Audio
from .animation import Animation
from .document import Document
from .dice import Dice
from .poll import Poll
from .game import Game
from .sticker import Sticker
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .contact import Contact
from .location import Location
from .venue import Venue
from .message_entity import MessageEntity
from .photo_size import PhotoSize
from .invoice import Invoice
from .successful_payment import SuccessfulPayment
from .passport_data import PassportData
from .inline_keyboard_markup import InlineKeyboardMarkup


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
    forward_signature = Field()
    forward_sender_name = Field()
    forward_date = Field()
    reply_to_message = Field()
    via_bot = Field()
    edit_date = Field()
    media_group_id = Field()
    author_signature = Field()
    text = Field()
    entities = Field()
    animation = Field()
    audio = Field()
    document = Field()
    photo = Field()
    sticker = Field()
    video = Field()
    video_note = Field()
    voice = Field()
    caption = Field()
    caption_entities = Field()
    contact = Field()
    dice = Field()
    game = Field()
    poll = Field()
    location = Field()
    venue = Field()
    new_chat_members = Field()
    new_chat_member = Field()       # Weird Fields that exist
    new_chat_participant = Field()  # in some messages but not in the doc
    left_chat_member = Field()
    left_chat_participant = Field()
    new_chat_title = Field()
    new_chat_photo = Field()
    delete_chat_photo = Field()
    group_chat_created = Field()
    supergroup_chat_created = Field()
    channel_chat_created = Field()
    migrate_to_chat_id = Field()
    migrate_from_chat_id = Field()
    pinned_message = Field()
    invoice = Field()
    successful_payment = Field()
    connected_website = Field()
    passport_data = Field()
    reply_markup = Field()

    def __init__(self,
                 message_id: int,
                 date: int,
                 chat: 'Chat',
                 from_user: User = None,
                 forward_from: User = None,
                 forward_from_chat: 'Chat' = None,
                 forward_from_message_id: int = None,
                 forward_signature: str = None,
                 forward_sender_name: str = None,
                 forward_date: int = None,
                 reply_to_message: 'Message' = None,
                 via_bot: User = None,
                 edit_date: int = None,
                 media_group_id: str = None,
                 author_signature: str = None,
                 text: str = None,
                 entities: List[MessageEntity] = None,
                 animation: Animation = None,
                 audio: Audio = None,
                 document: Document = None,
                 dice: Dice = None,
                 game: Game = None,
                 poll: Poll = None,
                 photo: List[PhotoSize] = None,
                 sticker: Sticker = None,
                 video: Video = None,
                 video_note: VideoNote = None,
                 voice: Voice = None,
                 caption: str = None,
                 caption_entities: List[MessageEntity] = None,
                 contact: Contact = None,
                 location: Location = None,
                 venue: Venue = None,
                 new_chat_members: User = None,
                 new_chat_member: User = None,
                 new_chat_participant: User = None,
                 left_chat_participant: User = None,
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
                 invoice: Invoice = None,
                 successful_payment: SuccessfulPayment = None,
                 connected_website: str = None,
                 passport_data: PassportData = None,
                 reply_markup: InlineKeyboardMarkup = None
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

        self.forward_signature = \
            Field(forward_signature, [str])

        self.forward_sender_name = \
            Field(forward_sender_name, [str])

        self.forward_date = \
            Field(forward_date, [int])

        self.reply_to_message = \
            Field(reply_to_message, [Message])

        self.via_bot = \
            Field(via_bot, [User])

        self.edit_date = \
            Field(edit_date, [int])

        self.media_group_id = \
            Field(media_group_id, [str])

        self.author_signature = \
            Field(author_signature, [str])

        self.text = \
            Field(text, [str])

        self.entities = \
            ListField(entities, [MessageEntity])

        self.animation = \
            Field(animation, [Animation])

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

        self.video_note = \
            Field(video_note, [VideoNote])

        self.voice = \
            Field(voice, [Voice])

        self.caption = \
            Field(caption, [str])

        self.caption_entities = \
            ListField(caption_entities, [MessageEntity])

        self.contact = \
            Field(contact, [Contact])

        self.location = \
            Field(location, [Location])

        self.venue = \
            Field(venue, [Venue])

        self.new_chat_members = \
            ListField(new_chat_members, [User])

        self.new_chat_member = \
            Field(new_chat_member, [User])

        self.new_chat_participant = \
            Field(new_chat_participant, [User])

        self.left_chat_participant = \
            Field(left_chat_participant, [User])

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

        self.invoice = \
            Field(invoice, [Invoice])

        self.successful_payment = \
            Field(successful_payment, [SuccessfulPayment])

        self.connected_website = \
            Field(connected_website, [str])

        self.passport_data = \
            Field(passport_data, [PassportData])

        self.reply_markup = \
            Field(reply_markup, [InlineKeyboardMarkup])




from .chat import Chat  # NOQA
