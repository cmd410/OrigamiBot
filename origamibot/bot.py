from typing import List, Optional

from httpx._types import ProxiesTypes

from ._hints import URLTypes, UpdateTypeStr
from .api import UpdateAPI, MessageAPI


class Bot(UpdateAPI, MessageAPI):
    def __init__(self,
                 token: str,
                 *,
                 host: URLTypes = 'https://api.telegram.org',
                 proxies: ProxiesTypes = None,
                 update_limit: Optional[int] = None,
                 update_timeout: Optional[int] = None,
                 allowed_updates: Optional[List[UpdateTypeStr]] = None,
                 ) -> None:

        params = locals().copy()
        del params['self']
        del params['token']

        super().__init__(token, **params)
