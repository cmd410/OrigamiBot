from .tg import DEFAULT_API_HOST


class Bot:
    def __init__(self,
                 token: str,
                 api_server: str=api_request.DEFAULT_API_HOST
                 ):
        self.token = token
        self.api_format_string = api_server + '/bot{token}/{method}'
    