from typing import Optional, List

from .api_base import APIBase
from ..types import Update


class PollingAPI(APIBase):
    """API for getting updates and setting webhooks
    """

    def get_updates(self,
                    offset: Optional[int] = None,
                    limit: Optional[int] = None,
                    timeout: Optional[int] = 30,
                    allowed_updates: Optional[List[str]] = None
                    ) -> List[Update]:
        return Update.from_list(self._simple_request('getUpdates', locals()))
