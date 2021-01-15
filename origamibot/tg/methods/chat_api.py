from typing import Optional, List

from .api_base import APIBase
from .util import own_result
from ..common_typings import ChatID
from ..types import Message, MessageEntity, InlineKeyboardMarkup


class ChatAPI(APIBase):
    """API for working with chats.
    Sending and editing messages
    """

    @own_result
    def send_message(self,
                     chat_id: ChatID,
                     text: str,
                     parse_mode: Optional[str] = None,
                     enities: Optional[List] = None,
                     disable_web_page_preview: Optional[bool] = None,
                     disable_notification: Optional[bool] = None,
                     reply_to_message_id: Optional[int] = None,
                     allow_sending_without_reply: Optional[bool] = None,
                     reply_markup: Optional = None,
                     ) -> Message:
        """Use this method to send text messages.
        On success, the sent Message is returned.
        """
        return Message.from_dict(self._simple_request("sendMessage", locals()))

    @own_result
    def edit_message_text(self,
                          text: str,
                          chat_id: Optional[ChatID] = None,
                          message_id: Optional[int] = None,
                          inline_message_id: Optional[str] = None,
                          parse_mode: Optional[str] = None,
                          entities: Optional[List[MessageEntity]] = None,
                          disable_web_page_preview: Optional[bool] = None,
                          reply_markup: Optional[InlineKeyboardMarkup] = None,
                          ) -> Message:
        """Use this method to edit text and game messages.
        On success, if the edited message is not an inline message,
        the edited Message is returned, otherwise True is returned.
        """
        return Message.from_dict(self._simple_request("editMessageText", locals()))
