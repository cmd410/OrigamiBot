from typing import List, Literal, Optional, Union
from io import IOBase

from ._base import APIBase
from .._hints import ChatID, ParseMode, ReplyMarkup
from ..types.message import Message
from ..types.message_id import MessageId


class MessageAPI(APIBase):
    """API that implements sending,
    editing and deleting messages
    """

    async def send_message(self,
                           chat_id: ChatID,
                           text: str,
                           parse_mode: Optional[ParseMode] = None,
                           # TODO message entities
                           entities: Optional[List[dict]] = None,
                           disable_web_page_preview: Optional[bool] = None,
                           disable_notification: Optional[bool] = None,
                           reply_to_message_id: Optional[int] = None,
                           allow_sending_without_reply: Optional[bool] = None,
                           # TODO reply markup
                           reply_markup: Optional[ReplyMarkup] = None
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

        return Message(
            **self._extract_request_result(
                await self._send_request(
                    'sendMessage',
                    data={
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
                )
            )
        )

    async def delete_message(self,
                             chat_id: ChatID,
                             message_id: int
                             ) -> Literal[True]:
        """Use this method to delete a message,
        including service messages, with the
        following limitations:

        * A message can only be deleted if it
            was sent less than 48 hours ago.
        * A dice message in a private chat can
            only be deleted if it was sent more
            than 24 hours ago.
        * Bots can delete outgoing messages in
            private chats, groups, and supergroups.
        * Bots can delete incoming messages in
            private chats.
        * Bots granted can_post_messages permissions
            can delete outgoing messages in channels.
        * If the bot is an administrator of a
            group, it can delete any message there.
        * If the bot has can_delete_messages
            permission in a supergroup or a channel,
            it can delete any message there.

        Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format ``@channelusername``)
        :param message_id: Identifier of the message to delete
        """
        return self._extract_request_result(
            await self._send_request(
                'deleteMessage',
                data={
                    'chat_id': chat_id,
                    'message_id': message_id
                }
            )
        )

    async def edit_message_text(self,
                                text: str,
                                chat_id: Optional[ChatID] = None,
                                message_id: Optional[int] = None,
                                inline_message_id: Optional[str] = None,
                                parse_mode: Optional[ParseMode] = None,
                                entities: Optional[dict] = None,
                                disable_web_page_preview: Optional[bool] = None,
                                reply_markup: Optional[ReplyMarkup] = None
                                ) -> Union[Message, Literal[True]]:
        """Use this method to edit text and game messages.

        On success, if the edited message is not
        an inline message, the edited Message is returned,
        otherwise True is returned.

        :param chat_id: Required if inline_message_id is
            not specified. Unique identifier for the target
            chat or username of the target channel(in the
            format @channelusername)
        :param message_id: Required if inline_message_id
            is not specified. Identifier of the message to edit
        :param inline_message_id: Required if chat_id and message_id
            are not specified. Identifier of the inline message
        :param text: New text of the message, 1-4096 characters
            after entities parsing
        :param parse_mode: Mode for parsing entities in the message text
        :param entities: List of special entities that appear in message
            text, which can be specified instead of parse_mode
        :param disable_web_page_preview: Disables link previews
            for links in this message
        :param reply_markup: A JSON-serialized object for an inline keyboard.
        """

        responce = self._extract_request_result(
            await self._send_request(
                'editMessageText',
                data={
                    'text': text,
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'inline_message_id': inline_message_id,
                    'parse_mode': parse_mode,
                    'entities': entities,
                    'disable_web_page_preview': disable_web_page_preview,
                    'reply_markup': reply_markup
                }
            )
        )

        if responce == True:
            return True
        else:
            return Message(**responce)

    async def edit_message_caption(self,
                                   caption: str,
                                   chat_id: Optional[ChatID] = None,
                                   message_id: Optional[int] = None,
                                   inline_message_id: Optional[str] = None,
                                   parse_mode: Optional[ParseMode] = None,
                                   caption_entities: Optional[dict] = None,
                                   reply_markup: Optional[ReplyMarkup] = None
                                   ) -> Union[Message, Literal[True]]:
        """Use this method to edit captions of messages.

        On success, if the edited message is not an inline
        message, the edited Message is returned,
        otherwise True is returned.
        """

        response = self._extract_request_result(
            await self._send_request(
                'editMessageCaption',
                data={
                    'caption': caption,
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'inline_message_id': inline_message_id,
                    'parse_mode': parse_mode,
                    'caption_entities': caption_entities,
                    'reply_markup': reply_markup
                }
            )
        )

        if response == True:
            return True
        else:
            return Message(**response)

    async def forward_message(self,
                              chat_id: ChatID,
                              from_chat_id: ChatID,
                              message_id: int,
                              disable_notification: Optional[bool] = None
                              ) -> Message:
        """Use this method to forward messages of any kind.

        Service messages can't be forwarded.

        On success, the sent Message is returned.

        :param chat_id: Unique identifier for the target
            chat or username of the target channel
            (in the format @channelusername)
        :param from_chat_id: Unique identifier for the
            chat where the original message was sent
            (or channel username in the format @channelusername)
        :param message_id:Message identifier in the chat
            specified in from_chat_id
        :param disable_notification: Sends the message silently.
            Users will receive a notification with no sound.
        """

        return Message(
            **self._extract_request_result(
                await self._send_request(
                    'forwardMessage',
                    data={
                        'chat_id': chat_id,
                        'from_chat_id': from_chat_id,
                        'message_id': message_id,
                        'disable_notification': disable_notification
                    }
                )
            )
        )

    async def copy_message(self,
                           chat_id: ChatID,
                           from_chat_id: ChatID,
                           message_id: int,
                           caption: Optional[str] = None,
                           parse_mode: Optional[ParseMode] = None,
                           caption_entities: Optional[List[dict]] = None,
                           disable_notification: Optional[bool] = None,
                           reply_to_message_id: Optional[int] = None,
                           allow_sending_without_reply: Optional[bool] = None,
                           reply_markup: Optional[ReplyMarkup] = None
                           ) -> MessageId:
        """Use this method to copy messages of any kind.

        Service messages and invoice messages can't be copied.

        The method is analogous to the method forward_message,
        but the copied message doesn't have a link to the
        original message.

        Returns the MessageId of the sent message on success.

        :param chat_id: Unique identifier for the target chat
            or username of the target channel (in the format
            @channelusername)
        :param from_chat_id: Unique identifier for the chat
            where the original message was sent (or channel
            username in the format @channelusername)
        :param message_id: Message identifier in the chat
            specified in from_chat_id
        :param caption: New caption for media, 0-1024
            characters after entities parsing. If not specified,
            the original caption is kept
        :param parse_mode: Mode for parsing entities in the new
            caption. See formatting options for more details.
        :param caption_entities: List of special entities that
            appear in the new caption, which can be specified
            instead of parse_mode
        :param disable_notification: Sends the message silently.
            Users will receive a notification with no sound.
        :param reply_to_message_id: If the message is a reply,
            ID of the original message
        :param allow_sending_without_reply: Pass True, if the
            message should be sent even if the specified
            replied-to message is not found
        :param reply_markup: Additional interface options.
            A JSON-serialized object for an inline keyboard,
            custom reply keyboard, instructions to remove
            reply keyboard or to force a reply from the user.
        """

        return MessageId(
                **self._extract_request_result(
                await self._send_request(
                    'copyMessage',
                    data={
                        'chat_id': chat_id,
                        'from_chat_id': from_chat_id,
                        'message_id': message_id,
                        'caption': caption,
                        'parse_mode': parse_mode,
                        'caption_entities': caption_entities,
                        'disable_notification': disable_notification,
                        'reply_to_message_id': reply_to_message_id,
                        'allow_sending_without_reply': allow_sending_without_reply,
                        'reply_markup': reply_markup
                    }
                )
            )
        )

    async def send_photo(self,
                         chat_id: ChatID,
                         photo: Union[IOBase, str],
                         caption: Optional[str] = None,
                         parse_mode: Optional[ParseMode] = None,
                         caption_entities: Optional[List[dict]] = None,
                         disable_notification: Optional[bool] = None,
                         reply_to_message_id: Optional[int] = None,
                         allow_sending_without_reply: Optional[bool] = None,
                         reply_markup: Optional[ReplyMarkup] = None
                         ) -> Message:
        """Use this method to send photos.

        On success, the sent Message is returned.

        :param chat_id: Unique identifier for the target
            chat or username of the target channel (in the
            format @channelusername)
        :param photo: Photo to send. Pass a file_id as String
            to send a photo that exists on the Telegram servers
            (recommended), pass an HTTP URL as a String for
            Telegram to get a photo from the Internet, or
            upload a new photo using multipart/form-data.
        :param caption: Photo caption (may also be used when
            resending photos by file_id), 0-1024 characters
            after entities parsing
        :param parse_mode: Mode for parsing entities in the
            photo caption. See formatting options for more
            details.
        :param caption_entities: List of special entities
            that appear in the caption, which can be specified
            instead of parse_mode
        :param disable_notification: Sends the message silently.
            Users will receive a notification with no sound.
        :param reply_to_message_id: If the message is a reply,
            ID of the original message
        :param allow_sending_without_reply: Pass True, if the
            message should be sent even if the specified replied-to
            message is not found
        :param reply_markup: Additional interface options.
            A JSON-serialized object for an inline keyboard,
            custom reply keyboard, instructions to remove reply
            keyboard or to force a reply from the user.
        """

        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'caption_entities': caption_entities,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': reply_markup,
        }

        if isinstance(photo, IOBase):
            files = {'photo': photo}
        else:
            data['photo'] = photo
            files = None

        return Message(
            **self._extract_request_result(
                await self._send_request(
                    'sendPhoto',
                    data=data,
                    files=files
                )
            )
        )

    async def send_audio(self,
                       chat_id: ChatID,
                       audio: Union[IOBase, str],
                       caption: Optional[str] = None,
                       parse_mode: Optional[ParseMode] = None,
                       caption_entities: Optional[List[dict]] = None,
                       duration: Optional[int] = None,
                       performer: Optional[str] = None,
                       title: Optional[str] = None,
                       thumb: Union[IOBase, str, None] = None
                       ) -> Message:
        data = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "duration": duration,
            "performer": performer,
            "title": title,
            "thumb": thumb,
        }

        if isinstance(audio, IOBase):
            files = {'audio': audio}
        else:
            data['audio'] = audio
            files = None
  
        return Message(
                **self._extract_request_result(
                    await self._send_request(
                        'sendAudio',
                        data=data,
                        files=files
                    )
                )
            )