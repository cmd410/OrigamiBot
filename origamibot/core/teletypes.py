"""All Telegram API types here"""

from dataclasses import dataclass, fields, is_dataclass
from inspect import getmembers
from sys import modules
from pprint import pprint


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str = None
    username: str = None
    language_code: str = None
    can_join_groups: bool = None
    can_read_all_group_messages: bool = None
    supports_inline_queries: bool = None


@dataclass
class PhotoSize:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int = None


@dataclass
class Animation:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: PhotoSize = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None


@dataclass
class Audio:
    file_id: str
    file_unique_id: str
    duration: int
    performer: str = None
    title: str = None
    mime_type: str = None
    file_size: int = None
    thumb: PhotoSize = None


@dataclass
class Document:
    file_id: str
    file_unique_id: str
    thumb: PhotoSize = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None


@dataclass
class MaskPosition:
    point: str
    x_shift: float
    y_shift: float
    scale: float


@dataclass
class Sticker:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    thumb: PhotoSize = None
    emoji: str = None
    set_name: str = None
    mask_position: MaskPosition = None
    file_size: int = None


@dataclass
class Video:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: PhotoSize = None
    mime_type: str = None
    file_size: int = None


@dataclass
class VideoNote:
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: PhotoSize = None
    file_size: int = None


@dataclass
class Contact:
    phone_number: str
    first_name: str
    last_name: str = None
    user_id: int = None
    vcard: str = None


@dataclass
class Dice:
    emoji: str
    value: int


@dataclass
class Game:
    title: str
    description: str
    photo: list
    text: str = None
    text_entities: list = None
    animation: Animation = None


@dataclass
class PollOption:
    text: str
    voter_count: int


@dataclass
class PollAnswer:
    poll_id: str
    user: User
    option_ids: list


@dataclass
class Poll:
    id: str
    question: str
    options: list
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: int = None
    explanation: str = None
    explanation_entities: list = None
    one_period: int = None
    close_date: int = None


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int
    url: str = None
    user: User = None
    language: str = None


@dataclass
class Voice:
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str = None
    file_size: int = None


@dataclass
class Location:
    longitude: float
    latitude: float


@dataclass
class Venue:
    location: Location
    title: str
    address: str
    foursquare_id: str = None
    foursquare_type: str = None


@dataclass
class UserProfilePhotos:
    total_count: int
    photos: list


@dataclass
class File:
    file_id: str
    file_unique_id: str
    file_size: int = None
    file_path: str = None


@dataclass
class ReplyKeyboardRemove:
    remove_keyboard: bool = True
    selective: bool = None


@dataclass
class KeyboardButtonPollType:
    type: str = None


@dataclass
class KeyboardButton:
    text: str
    request_contact: bool = None
    request_location: bool = None
    request_poll: KeyboardButtonPollType = None


@dataclass
class ReplyKeyboardMarkup:
    keyboard: list
    resize_keyboard: bool = None
    one_time_keyboard: bool = None
    selective: bool = None


@dataclass
class Invoice:
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


@dataclass
class ShippingAddress:
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


@dataclass
class OrderInfo:
    name: str = None
    phone_number: str = None
    email: str = None
    shipping_address: ShippingAddress = None


@dataclass
class SuccessfulPayment:
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    shipping_option_id: str = None
    order_info: OrderInfo = None


@dataclass
class EncryptedCredentials:
    data: str
    hash: str
    secret: str


@dataclass
class PassportFile:
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


@dataclass
class ForceReply:
    selective: bool
    force_reply: bool = True


@dataclass
class EncryptedPassportElement:
    type: str
    data: str
    hash: str
    phone_number: str = None
    email: str = None
    files: list = None
    front_side: PassportFile = None
    reverse_side: PassportFile = None
    selfie: PassportFile = None
    translation: PassportFile = None


@dataclass
class PassportData:
    data: EncryptedPassportElement
    credentials: EncryptedCredentials


@dataclass
class LoginUrl:
    url: str
    forward_text: str = None
    bot_username: str = None
    request_write_access: bool = None


@dataclass
class CallbackGame:
    # Placeholder class, does not contain info
    pass


@dataclass
class InlineKeyboardButton:
    text: str
    url: str = None
    login_url: LoginUrl = None
    callback_data: str = None
    switch_inline_query: str = None
    switch_inline_query_current_chat: str = None
    callback_game: CallbackGame = None
    pay: bool = None


@dataclass
class InlineKeyboardMarkup:
    inline_keyboard: list


@dataclass
class InputMediaPhoto:
    type: str
    media: str
    caption: str = None
    parse_mode: str = None


@dataclass
class InputMediaVideo:
    type: str
    media: str
    thumb: str = None
    caption: str = None
    parse_mode: str = None
    width: int = None
    height: int = None
    duration: int = None
    supports_streaming: bool = None


@dataclass
class InputMediaAnimation:
    type: str
    media: str
    thumb: str = None
    caption: str = None
    parse_mode: str = None
    width: int = None
    height: int = None
    duration: int = None


@dataclass
class InputMediaAudio:
    type: str
    media: str
    thumb: str = None
    caption: str = None
    parse_mode: str = None
    width: int = None
    height: int = None
    duration: int = None
    title: str = None


@dataclass
class InputMediaDocument:
    type: str
    media: str
    thumb: str = None
    caption: str = None
    parse_mode: str = None


@dataclass
class ResponseParameters:
    migrate_to_chat_id: int = None
    retry_after: int = None


@dataclass
class BotCommand:
    command: str
    description: str


@dataclass
class ChatMember:
    user: User
    status: str
    custom_title: str = None
    until_date: int = None
    can_be_edited: bool = None
    can_post_messages: bool = None
    can_edit_messages: bool = None
    can_delete_messages: bool = None
    can_restrict_members: bool = None
    can_promote_members: bool = None
    can_change_info: bool = None
    can_invite_users: bool = None
    can_pin_messages: bool = None
    is_member: bool = None
    can_send_messages: bool = None
    can_send_media_messages: bool = None
    can_send_polls: bool = None
    can_send_other_messages: bool = None
    can_add_web_page_previews: bool = None


@dataclass
class ChatPhoto:
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


@dataclass
class ChatPermissions:
    can_send_messages: bool = None
    can_send_media_messages: bool = None
    can_send_polls: bool = None
    can_send_other_messages: bool = None
    can_add_web_page_previews: bool = None
    can_change_info: bool = None
    can_invite_users: bool = None
    can_pin_messages: bool = None


@dataclass
class Message:
    message_id: int
    date: int
    chat: 'Chat'
    from_user: User = None
    forward_from: User = None
    forward_from_chat: User = None
    forward_from_message_id: int = None
    forward_signature: str = None
    forward_sender_name: str = None
    forward_date: int = None
    reply_to_message: 'Message' = None
    via_bot: User = None
    edit_date: int = None
    media_group_id: str = None
    author_signature: str = None
    text: str = None
    entities: list = None
    animation: Animation = None
    audio: Audio = None
    document: Document = None
    photo: list = None
    sticker: Sticker = None
    video: Video = None
    video_note: VideoNote = None
    voice: Voice = None
    caption: str = None
    caption_entities: list = None
    contact: Contact = None
    dice: Dice = None
    game: Game = None
    poll: Poll = None
    venue: Venue = None
    location: Location = None
    new_chat_members: list = None
    left_chat_member: User = None
    new_chat_title: str = None
    new_chat_photo: list = None
    delete_chat_photo: bool = None
    group_chat_created: bool = None
    supergroup_chat_created: bool = None
    channel_chat_created: bool = None
    migrate_to_chat_id: int = None
    migrate_from_chat_id: int = None
    pinned_message: 'Message' = None
    invoice: Invoice = None
    successful_payment: SuccessfulPayment = None
    connected_website: str = None
    passport_data: PassportData = None
    reply_markup: InlineKeyboardMarkup = None


@dataclass
class CallbackQuery:
    id: str
    from_user: User
    chat_instance: str
    message: Message = None
    inline_message_id: str = None
    data: str = None
    game_short_name: str = None


@dataclass
class Chat:
    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    chat_photo: ChatPhoto = None
    description: str = None
    invite_link: str = None
    pinned_message: Message = None
    permissions: ChatPermissions = None
    slow_mode_delay: int = None
    sticker_set_name: str = None
    can_set_sticker_set: bool = None


@dataclass
class Update:
    update_id: int
    message: Message = None
    edited_message: Message = None
    channel_post: Message = None
    edited_channel_post: Message = None


# Collect all dataclasses in this module
api_types = [
    i[1] for i in getmembers(modules[__name__],
                             lambda item: is_dataclass(item))
    ]


api_types = sorted(
    api_types,
    key=lambda cls: len(fields(cls)),
    reverse=True)


__all__ = api_types


def native_type(dic: dict):
    """Recursively converts given dict into suitable dataclass"""

    if 'from' in dic.keys():
        dic['from_user'] = dic.pop('from')

    data_fields = set(dic.keys())
    for key, value in dic.items():
        if isinstance(value, dict):
            dic[key] = native_type(value)
        elif isinstance(value, list):
            for i, d in enumerate(value):
                value[i] = native_type(d)
     
    for cls in api_types:
        type_fields = set([i.name for i in fields(cls)])
        if data_fields.issubset(type_fields):
            try:
                return cls(**dic)
            except TypeError:   # On missing required arguments
                continue
    return dic
