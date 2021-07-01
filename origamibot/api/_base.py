from ..core.client import TelegramClient
from .._hints import JSON
from ..exceptions import TelegramAPIError


class APIBase:
    """Base class for all API classes
    """
    
    def __init__(self, token: str, **params) -> None:
        host = params.get('host', 'https://api.telegram.org')
        proxies = params.get('proxies', None)
        
        self._client = TelegramClient(
            host=host,
            proxies=proxies
        )
        self.__token = token

    async def _send_request(self, endpoint: str, data=None, files=None) -> JSON:
        return await self._client.arequest(self.__token,
                                           endpoint=endpoint,
                                           data=data,
                                           files=files
                                           )

    @staticmethod
    def _extract_request_result(response: dict) -> JSON:
        """Returns 'result' field from API response or
        raises a TelegramAPIError
        """
        if response['ok']:
            return response['result']
        else:
            code = response['error_code']
            description = response['description']
            raise TelegramAPIError(f'[{code}] {description}')
