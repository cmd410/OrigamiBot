from gevent import spawn, joinall

from genki.http.url import URL

from .tg.types import Update
from .tg.methods import PollingAPI, ChatAPI
from .tg.methods.util import DEFAULT_API_SERVER, addr


class Bot(PollingAPI, ChatAPI):
    """Bot class inherits all APIs plus
    manages registering dispatchers.(TODO)
    """
    def __init__(self,
                 token: str,
                 host: addr = DEFAULT_API_SERVER,
                 request_retries=5,
                 polling_interval: float = 30.0
                 ):
        super().__init__(token=token, host=host, request_retries=request_retries)
        self.polling_interval = polling_interval
        self.last_update_id = 0

    def process_update(self, update: Update):
        print(update.message)

    def start_polling(self):
        while True:
            updates = self.get_updates(offset=self.last_update_id + 1)
            if updates:
                self.last_update_id = max([i.update_id for i in updates])
                joinall([
                    spawn(self.process_update, upd)
                    for upd in updates
                ])
