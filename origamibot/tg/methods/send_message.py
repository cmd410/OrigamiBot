from typing import Union, List, Optional

from . import ChatID
from .api_request import APIRequest
from ..types import Message


class SendMessage(APIRequest, method='sendMessage'):
    """Use this method to send text messages.
    On success, the sent Message is returned.
    """

    def __call__(self,
                 token: str,
                 chat_id: ChatID,
                 text: str,
                 parse_mode: Optional[str] = None,
                 enities: Optional[List] = None,
                 disable_web_page_preview: Optional[bool] = None,
                 disable_notification: Optional[bool] = None,
                 reply_to_message_id: Optional[int] = None,
                 allow_sending_without_reply: Optional[bool] = None,
                 reply_markup: Optional = None
                 ) -> Message:
        data = {
            key: value
            for key, value in locals().items()
            if key not in {'self', 'token'}
        }

        responce = self.send_data(token,
                                  self.purify_args(data)
                                  )
        
        message = self.unwrap_result(responce)

        return Message.from_dict(message)


send_message = SendMessage()
