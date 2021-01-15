from typing import Optional, List, Union

from .api_base import APIBase
from .util import own_result
from ..common_typings import ChatID
from ..types import (Message,
                     MessageEntity,
                     InputMedia,
                     InlineKeyboardMarkup)


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
                          ) -> Union[Message, bool]:
        """Use this method to edit text and game messages.
        On success, if the edited message is not an inline message,
        the edited Message is returned, otherwise True is returned.
        """
        assert (chat_id and message_id) or inline_message_id
        result = self._simple_request("editMessageText", locals())
        if isinstance(result, dict):
            return Message.from_dict(result)
        else:
            return result

    def edit_message_caption(self,
                             chat_id: Optional[ChatID] = None,
                             message_id: Optional[int] = None,
                             inline_message_id: Optional[str] = None,
                             caption: Optional[str] = None,
                             parse_mode: Optional[str] = None,
                             caption_entities: Optional[List[MessageEntity]] = None,
                             reply_markup: Optional[InlineKeyboardMarkup] = None,
                             ) -> Union[Message, bool]:
        """Use this method to edit captions of messages.
        On success, if the edited message is not an inline message,
        the edited Message is returned, otherwise True is returned.
        """
        assert (chat_id and message_id) or inline_message_id
        result = self._simple_request("editMessageCaption", locals())
        if isinstance(result, dict):
            return Message.from_dict(result)
        else:
            return result

    def edit_message_media(self,
                           media: InputMedia,
                           chat_id: Optional[ChatID] = None,
                           message_id: Optional[int] = None,
                           inline_message_id: Optional[str] = None,
                           reply_markup: Optional[InlineKeyboardMarkup] = None
                           ):
        """Use this method to edit animation,
        audio, document, photo, or video messages.

        If a message is part of a message album,
        then it can be edited only to an audio
        for audio albums, only to a document
        for documentalbums and to a photo or a video
        otherwise. When an inline message is edited,
        a new file can't be uploaded.
        Use a previously uploaded file via its
        file_id or specify a URL.

        On success,
        if the edited message was sent by the bot,
        the edited Message is returned,
        otherwise True is returned.
        """
        assert (chat_id and message_id) or inline_message_id
        result = self._simple_request("editMessageMedia", locals())
        if isinstance(result, dict):
            return Message.from_dict(result)
        else:
            return result
