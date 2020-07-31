from .base import TelegramStructure, Field, ListField


class WebhookInfo(TelegramStructure):

    url = Field()
    has_custom_certificate = Field()
    pending_update_count = Field()
    last_error_date = Field()
    last_error_message = Field()
    max_connections = Field()
    allowed_update = Field()

    def __init__(self,
                 url: str,
                 has_custom_certificate: bool,
                 pending_update_count: int,
                 last_error_date: int = None,
                 last_error_message: str = None,
                 max_connections: int = None,
                 allowed_update: list = None
                 ):
        self.url = \
            Field(url, [str])

        self.has_custom_certificate = \
            Field(has_custom_certificate, [bool])

        self.pending_update_count = \
            Field(pending_update_count, [int])

        self.last_error_date = \
            Field(last_error_date, [int])

        self.last_error_message = \
            Field(last_error_message, [str])

        self.max_connections = \
            Field(max_connections, [int])

        self.allowed_update = \
            ListField(allowed_update, [str])
