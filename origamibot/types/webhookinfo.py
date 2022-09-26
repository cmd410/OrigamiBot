from typing import Optional, List

from .._hints import UpdateTypeStr
from ._base import TelegramObject


class WebhookInfo(TelegramObject):
    """Contains information about the
    current status of a webhook.
    """

    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str]
    last_error_date: Optional[int]
    last_error_message: Optional[str]
    max_connections: Optional[int]
    allowed_updates: Optional[List[UpdateTypeStr]]
