import requests
import json

from typing import List

from .teletypes import native_type, Update


api_url = 'https://api.telegram.org/bot{token}/{method}'


def request(token, method, data=dict()):
    """Make a raw api request.

    Returns result as dataclass or list of dataclasses
    Or dict if could not comprehend type
    """
    url = api_url.format(token=token, method=method)

    responce = requests.post(url, data)

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
