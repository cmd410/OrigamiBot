import requests
import json

from dataclasses import asdict
from typing import List, Union, Optional, IO

from .teletypes import (native_type,
                        Update,
                        User,
                        Message,
                        ReplyKeyboardMarkup,
                        ReplyKeyboardRemove,
                        ForceReply,
                        InlineKeyboardMarkup)


api_url = 'https://api.telegram.org/bot{token}/{method}'


def request(token, method, data=dict(), files=dict()):
    """Make a raw api request.

    Returns result as dataclass or list of dataclasses
    Or dict if could not comprehend type
    """
    url = api_url.format(token=token, method=method)

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
                 reply_to_message_id: Optional[int] = None) -> Message:
    """Use this method to send text messages.
    
    On success, the sent Message is returned.
    """
    data = {
        key: value
        for key, value in {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }.items()
        if value is not None
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
    }
    if disable_notification is not None:
        data['disable_notification'] = disable_notification

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
               reply_markup: Optional[Union[
                   InlineKeyboardMarkup,
                   ReplyKeyboardMarkup,
                   ReplyKeyboardRemove,
                   ForceReply
               ]] = None
               ) -> Message:
    """Use this method to send photos.

    On success, the sent Message is returned.
    """
    data = {
        key: value
        for key, value in {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (asdict(reply_markup)
                             if reply_markup is not None else None)
        }.items()
        if value is not None
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
