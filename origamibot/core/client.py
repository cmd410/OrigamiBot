import asyncio
from typing import Optional
import weakref
from _pytest.config import exceptions

from yarl import URL
from httpx import AsyncClient
from httpx._types import ProxiesTypes
from httpx._exceptions import RequestError
from pydantic import BaseModel

from .._hints import URLTypes, JSON
from ..exceptions import ClientError


class TelegramClient:
    """The low-level request sender, response reciever
    """
    
    def __init__(self,
                 host: URLTypes = 'https://api.telegram.org',
                 proxies: ProxiesTypes = None
                 ) -> None:
        if isinstance(host, URL):
            self.host = host
        else:
            self.host = URL(host)
        
        self._aclient = AsyncClient(proxies=proxies)
        
        weakref.finalize(self, self.close)
    
    def url_for(self, token: URLTypes, endpoint: URLTypes) -> URL:
        """Return url for bot endpoint
        """
        return self.host / f'bot{token}' / endpoint
    
    async def aclose(self):
        await self._aclient.aclose()
    
    def close(self):
        if self._aclient.is_closed:
            return
        asyncio.shield(self.aclose())
    
    async def arequest(self,
                       token: str,
                       endpoint: str,
                       data: Optional[dict] = None,
                       files: Optional[dict] = None
                       ) -> JSON:
        """Send request asynchronously.
        
        Takes bot token, endpoint and optionally data and files.
        """
        payload = {
            'url': str(self.url_for(token, endpoint))
        }
        
        if files:
            payload['files'] = files
        
        if data:
            data = {
                key: value if not isinstance(value, BaseModel) else value.dict()
                for key, value in data.items()
                if value is not None
            }
        
        if data and not files:
            payload['json'] = data
        elif data and files:
            payload['params'] = data

        try:
            r = await self._aclient.post(
                **payload
            )
        except RequestError as e:
            raise ClientError from e

        return r.json()
