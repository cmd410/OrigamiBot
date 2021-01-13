from abc import ABC

from ..tg import DEFAULT_API_HOST


class BotBase(ABC):
    """Base class for bots
    """

    def __init__(self,
                 token: str,
                 api_server: str = DEFAULT_API_HOST
                 ):
        self.token = token
        self.api_server = api_server
