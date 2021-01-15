import json
from typing import Union
from abc import ABC

from genki import post, Response
from genki.http.url import URL

from . import DEFAULT_API_SERVER
from ..exceptions import TelegramAPIError


addr = Union[URL, str]


class APIBase(ABC):
    """Base class that implements basic methods to send requests
    to TelegramAPI
    """

    def url_for(self, method: str) -> str:
        """Returns url for given method
        """
        return f"{str(self.host)}bot{self.token}/{method}"

    def _unwrap_result(self, responce: Response) -> Union[dict, list]:
        is_ok = False
        result = None

        json_obj = json.loads(responce.body)
        assert isinstance(json_obj, dict)
        assert "ok" in json_obj

        if json_obj["ok"]:
            is_ok = True
            result = json_obj["result"]
        else:
            is_ok = False
            result = json_obj["description"]

        if is_ok:
            return result
        else:
            raise TelegramAPIError(f"[{responce.status_code}] {result}")

    def _send_request(self, method: str, data: dict = {}, files: dict = {}) -> Response:
        """Sends request to server, returns Reponce object"""
        if files:
            raise NotImplementedError("Sending files is not supported yet.")
        return post(self.url_for(method), data=data).result()

    def _purify_data(self, data: dict) -> dict:
        """Returns dict with no None fields
        and removes self from it, usually used with locals() in methods
        """
        return {
            key: (
                self._purify_data(value)
                if isinstance(value, dict)
                else value
                )
            for key, value in data.items()
            if value is not None and key != "self"
        }

    def _simple_request(self, method: str, data: dict) -> Union[dict, list]:
        """Helper method for simple requests
        sends data dict and returns result field from server.
        """
        data = self._purify_data(data)
        responce = self._send_request(method, data)
        return self._unwrap_result(responce)

    def __init__(self, token: str, host: addr = DEFAULT_API_SERVER):
        self.token = token

        assert isinstance(host, (str, URL))
        if isinstance(host, str):
            self.host = URL(host)
        else:
            self.host = host
