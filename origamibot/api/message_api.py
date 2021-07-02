from typing import List, Optional

from ._base import APIBase
from .._hints import ChatID, ParseMode
from ..types.message import Message


class MessageAPI(APIBase):
    """API that implements sending,
    editing and deleting messages
    """
    
    def __init__(self, token: str, **params) -> None:
        super().__init__(token, **params)

    async def send_message(self,
                           chat_id: ChatID,
                           text: str,
                           parse_mode: Optional[ParseMode] = None,
                           entities: Optional[List[dict]] = None,  # TODO message entities
                           disable_web_page_preview: Optional[bool] = None,
                           disable_notification: Optional[bool] = None,
                           reply_to_message_id: Optional[int] = None,
                           allow_sending_without_reply: Optional[bool] = None,
                           reply_markup: Optional[dict] = None  # TODO reply markup
                           ) -> Message:
        """Use this method to send text messages.
        
        On success, the sent Message is returned.
        
        :param chat_id: Unique identifier for the
            target chat or username of the target channel
            (in the format @channelusername)
        :param text: Text of the message to be sent,
            1-4096 characters after entities parsing
        :param parse_mode: Mode for parsing entities in the message text.
        :param entities: List of special entities that appear in message
            text, which can be specified instead of parse_mode
        :param disable_web_page_preview: Disables link previews for
            links in this message
        :param disable_notification: Sends the message silently.
            Users will receive a notification with no sound.
        :param reply_to_message_id: If the message is a reply,
            ID of the original message
        :param allow_sending_without_reply: Pass True, if the message
            should be sent even if the specified replied-to message is not found
        :param reply_markup: Additional interface options. A JSON-serialized
            object for an inline keyboard, custom reply keyboard, instructions
            to remove reply keyboard or to force a reply from the user.
        """
        
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'entities': entities,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': reply_markup
        }
        
        return Message.construct(
            **self._extract_request_result(
                await self._send_request(
                    'sendMessage',
                    data=data
                )
            )
        )
    