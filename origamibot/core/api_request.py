import requests
import json

from dataclasses import asdict
from typing import List, Union, Optional, IO

from .teletypes import (
    native_type,
    Update,
    User,
    Message,
    ReplyMarkup,
    InlineKeyboardMarkup)


api_url = 'https://api.telegram.org/bot{token}/{method}'


def request(token, method, data=dict(), files=dict()):
    """Make a raw api request.

    Returns result as dataclass or list of dataclasses
    Or dict if could not comprehend type
    """
    url = api_url.format(token=token, method=method)

    data = {
        key: value
        for key, value in data.items()
        if value is not None
    }

    files = {
        key: value
        for key, value in files.items()
        if value is not None
    }

    responce = requests.post(url, data, files=files)

    if responce.status_code != 200:
        raise Exception(f'Server returned error: {responce.status_code}')

    data = json.loads(responce.text)['result']

    if isinstance(data, dict):
        return native_type(data)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = native_type(item)
    return data


def get_updates(token: str,
                offset: int = 0,
                limit: int = 100,
                allowed_updates: list = []) -> List[Update]:
    """Make getUpdate request to telegram API. Return list of updates"""

    updates = request(
        token,
        'getUpdates',
        data={
            'offset': offset + 1,
            'limit': limit,
            'allowed_updates': allowed_updates}
        )
    return updates


def get_me(token: str) -> User:
    """A simple method for testing your bot's auth token.

    Returns basic information about the bot in form of a User object.
    """
    return request(
        token,
        'getMe'
        )


def send_message(token: str,
                 chat_id: Union[int, str],
                 text: str,
                 parse_mode: Optional[str] = None,
                 disable_web_page_preview: Optional[bool] = None,
                 disable_notification: Optional[bool] = None,
                 reply_to_message_id: Optional[int] = None,
                 reply_markup: Optional[ReplyMarkup] = None) -> Message:
    """Use this method to send text messages.

    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }
    return request(
        token,
        'sendMessage',
        data
    )


def forward_message(token: str,
                    chat_id: Union[int, str],
                    from_chat_id: Union[int, str],
                    message_id: int,
                    disable_notification: Optional[bool] = None) -> Message:
    """Use this method to forward messages of any kind.

    On success, the sent Message is returned.
    """
    data = {
        'chat_id': chat_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id,
        'disable_notification': disable_notification
    }

    return request(
        token,
        'forwardMessage',
        data
    )


def send_photo(token: str,
               chat_id: Union[int, str],
               photo: Union[str, IO],
               caption: Optional[str] = None,
               parse_mode: Optional[str] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None
               ) -> Message:
    """Use this method to send photos.

    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }
    if not isinstance(photo, str):
        return request(token,
                       'sendPhoto',
                       data,
                       files={
                           'photo': photo
                       })
    else:
        data['photo'] = photo
        return request(token,
                       'sendPhoto',
                       data)


def send_audio(token: str,
               chat_id: Union[int, str],
               audio: Union[str, IO],
               caption: Optional[str] = None,
               parse_mode: Optional[str] = None,
               duration: Optional[int] = None,
               performer: Optional[str] = None,
               title: Optional[str] = None,
               thumb: Optional[Union[str, IO]] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None
               ) -> Message:
    """Use this method to send audio files.

    Your audio must be in the .MP3 or .M4A format.
    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'title': title,
            'performer': performer,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }
    files = dict()
    if isinstance(audio, str):
        data['audio'] = audio
    else:
        files['audio'] = audio

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendAudio',
        data,
        files
    )


def send_document(token: str,
                  chat_id: Union[int, str],
                  document: Union[str, IO],
                  thumb: Optional[Union[str, IO]] = None,
                  caption: Optional[str] = None,
                  parse_mode: Optional[str] = None,
                  disable_notification: Optional[bool] = None,
                  reply_to_message_id: Optional[int] = None,
                  reply_markup: Optional[ReplyMarkup] = None
                  ) -> Message:
    """Use this method to send general files.

    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }

    files = dict()
    if isinstance(document, str):
        data['document'] = document
    else:
        files['document'] = document

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendDocument',
        data,
        files
    )


def send_video(token: str,
               chat_id: Union[int, str],
               video: Union[str, IO],
               duration: Optional[int] = None,
               width: Optional[int] = None,
               height: Optional[int] = None,
               thumb: Optional[Union[str, IO]] = None,
               caption: Optional[str] = None,
               parse_mode: Optional[str] = None,
               supports_streaming: Optional[bool] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None
               ) -> Message:
    """Use this method to send video files.

    Telegram clients support mp4 videos (other formats may be sent as Document)
    On success, the sent Message is returned.
    """
    data = {
            'chat_id': chat_id,
            'caption': caption,
            'height': height,
            'width': width,
            'duration': duration,
            'parse_mode': parse_mode,
            'supports_streaming': supports_streaming,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }

    files = dict()
    if isinstance(video, str):
        data['video'] = video
    else:
        files['video'] = video

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendVideo',
        data,
        files
    )


def send_animation(token: str,
                   chat_id: Union[int, str],
                   animation: Union[str, IO],
                   duration: Optional[int] = None,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   thumb: Optional[Union[str, IO]] = None,
                   caption: Optional[Union[str, IO]] = None,
                   parse_mode: Optional[str] = None,
                   disable_notification: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   reply_markup: Optional[ReplyMarkup] = None
                   ) -> Message:
    """Use this method to send animation files (GIF or video without sound).

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'duration': duration,
        'width': width,
        'height': height,
        'caption': caption,
        'parse_mode': parse_mode,
        'disable_notification': disable_notification,
        'reply_to_message_id': disable_notification,
        'reply_markup': (asdict(reply_markup)
                         if reply_markup is not None else None)
    }

    files = dict()
    if isinstance(animation, str):
        data['animation'] = animation
    else:
        files['animation'] = animation

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendAnimation',
        data,
        files
    )


def send_voice(token: str,
               chat_id: Union[int, str],
               voice: Union[str, IO],
               caption: Optional[str] = None,
               parse_mode: Optional[str] = None,
               duration: Optional[int] = None,
               disable_notification: Optional[bool] = None,
               reply_to_message_id: Optional[int] = None,
               reply_markup: Optional[ReplyMarkup] = None
               ) -> Message:
    """Use this method to send audio files to display the file as a voice message.

    For this to work, your audio must be in an .OGG file encoded with OPUS.
    On success, the sent Message is returned.
    """
    data = {
        'chat_id': chat_id,
        'duration': duration,
        'caption': caption,
        'parse_mode': parse_mode,
        'disable_notification': disable_notification,
        'reply_to_message_id': disable_notification,
        'reply_markup': (asdict(reply_markup)
                         if reply_markup is not None else None)
    }

    files = dict()
    if isinstance(voice, str):
        data['voice'] = voice
    else:
        files['voice'] = voice

    return request(
        token,
        'sendVoice',
        data,
        files
    )


def send_video_note(token: str,
                    chat_id: Union[int, str],
                    video_note: Union[str, IO],
                    duration: Optional[int] = None,
                    length: Optional[int] = None,
                    thumb: Optional[Union[str, IO]] = None,
                    disable_notification: Optional[bool] = None,
                    reply_to_message_id: Optional[int] = None,
                    reply_markup: Optional[ReplyMarkup] = None
                    ) -> Message:
    """Use this method to send rounded square mp4 videos of up to 1 minute long.

    On success, the sent Message is returned."""
    data = {
            'chat_id': chat_id,
            'duration': duration,
            'length': length,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }

    files = dict()
    if isinstance(video_note, str):
        data['video_note'] = video_note
    else:
        files['video_note'] = video_note

    if isinstance(thumb, str):
        data['thumb'] = thumb
    else:
        files['thumb'] = thumb

    return request(
        token,
        'sendVideoNote',
        data,
        files
    )


def send_location(token: str,
                  chat_id: Union[int, str],
                  latitude: float,
                  longitude: float,
                  live_period: Optional[int] = None,
                  disable_notification: Optional[bool] = None,
                  reply_to_message_id: Optional[int] = None,
                  reply_markup: Optional[ReplyMarkup] = None
                  ) -> Message:
    """Use this method to send point on the map.

    On success, the sent Message is returned.
    """

    data = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'live_period': live_period,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup
    }

    return request(
        token,
        'sendLocation',
        data
    )


def edit_message_live_location(token: str,
                               latitude: float,
                               longitude: float,
                               chat_id: Optional[Union[int, str]] = None,
                               message_id: Optional[int] = None,
                               inline_message_id: Optional[str] = None,
                               reply_markup:
                               Optional[InlineKeyboardMarkup] = None
                               ) -> Union[Message, bool]:
    """Use this method to edit live location messages.

    A location can be edited until its live_period expires
    or editing is explicitly disabled by a call to stopMessageLiveLocation.

    On success, if the edited message was sent by the bot,
    the edited Message is returned, otherwise True is returned.
    """
    data = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup
    }

    return request(
        token,
        'editMessageLiveLocation',
        data
    )


def stop_message_live_location(token: str,
                               chat_id:
                               Optional[Union[int, str]] = None,
                               message_id:
                               Optional[int] = None,
                               inline_message_id:
                               Optional[str] = None,
                               reply_markup:
                               Optional[ReplyMarkup] = None,
                               ) -> Union[Message, bool]:
    """Use this method to stop updating a live location message.

    On success, if the message was sent by the bot,
    the sent Message is returned,
    otherwise True is returned
    """

    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup
    }

    return request(
        token,
        'stopMessageLiveLocation',
        data
    )
