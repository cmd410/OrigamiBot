from .base import TelegramStructure, InlineQueryResult, InputMessageContent

from .animation import Animation
from .audio import Audio
from .bot_command import BotCommand
from .callback_query import CallbackQuery
from .chat import Chat
from .chat_member import ChatMember
from .chat_permissions import ChatPermissions
from .chat_photo import ChatPhoto
from .chosen_inline_result import ChosenInlineResult
from .contact import Contact
from .dice import Dice
from .document import Document
from .encrypted_credentials import EncryptedCredentials
from .encrypted_passport_element import EncryptedPassportElement
from .file import File
from .force_reply import ForceReply
from .game import Game
from .invoice import Invoice
from .labeled_price import LabeledPrice
from .location import Location
from .login_url import LoginUrl
from .mask_position import MaskPosition
from .message import Message
from .message_entity import MessageEntity
from .order_info import OrderInfo
from .passport_data import PassportData
from .passport_file import PassportFile
from .photo_size import PhotoSize
from .poll import Poll
from .poll_answer import PollAnswer
from .poll_option import PollOption
from .pre_checkout_query import PreCheckoutQuery
from .responce_parameters import ResponseParameters
from .shipping_address import ShippingAddress
from .shipping_option import ShippingOption
from .shipping_query import ShippingQuery
from .sticker import Sticker
from .successful_payment import SuccessfulPayment
from .update import Update
from .user import User
from .user_profile_photos import UserProfilePhotos
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .webhook_info import WebhookInfo

from .inline_keyboard_button import InlineKeyboardButton
from .inline_keyboard_markup import InlineKeyboardMarkup
from .reply_keyboard_markup import ReplyKeyboardMarkup
from .reply_keyboard_remove import ReplyKeyboardRemove
from .keyboard_button import KeyboardButton
from .keyboard_button_poll_type import KeyboardButtonPollType

from .inline_query import InlineQuery

from .input_file import InputFile

from .input_location_message_content import InputLocationMessageContent
from .input_text_message_content import InputTextMessageContent
from .input_contact_message_content import InputContactMessageContent
from .input_venue_message_content import InputVenueMessageContent

from .input_media_animation import InputMediaAnimation
from .input_media_audio import InputMediaAudio
from .input_media_document import InputMediaDocument
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo

from typing import Union

ReplyMarkup = Union[
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup
    ]

InputMedia = Union[
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo
]
