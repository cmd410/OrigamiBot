from functools import wraps
from typing import Union, List
from collections.abc import Callable
from json import loads

from genki import post, Response

from .. import DEFAULT_API_HOST
from ..types import TelegramType
from ..exceptions import TelegramAPIError


class APIRequest(Callable):
    """Abstract base class for all API request objects
    """

    method: str = ''

    def __init_subclass__(cls, /, method: str, **kwargs):
        super().__init_subclass__(**kwargs)
        assert method, "Attempt to create API method without method string"
        cls.method = method

    def __init__(self, host: str = DEFAULT_API_HOST):
        self.host = host

    def get_request_url(self,
                        token: str,
                        ) -> str:
        return f'{self.host}/bot{token}/{self.method}'

    def send_data(self,
                  token: str,
                  data: dict = {},
                  files: dict = {}
                  ) -> Response:
        url = self.get_request_url(token)
        if files:
            # TODO sending files
            raise NotImplementedError('Sending files is not supported yet')
        return post(url, data=data).result()

    @staticmethod
    def purify_args(data: dict) -> dict:
        return {
            key: value
            for key, value in data.items()
            if value is not None
        }

    def unwrap_result(self, responce: Response) -> Union[dict, list]:
        """Returns "result" field of API response or raises error
        """
        data = responce.body

        json_obj = loads(data)

        assert isinstance(json_obj, dict)
        assert 'ok' in json_obj

        if json_obj['ok']:
            return json_obj['result']
        else:
            raise TelegramAPIError(
                f'[{responce.status_code}]'
                f'{json_obj.get("description", "No description")}'
            )

    @staticmethod
    def map_data(data: Union[dict, list],
                 type=TelegramType
                 ) -> Union[TelegramType, List[TelegramType]]:
        return type.from_data(data)

    @classmethod
    def with_host(cls, host: str):
        """Return APIRequest object with custom host.
        """
        return cls(host)
