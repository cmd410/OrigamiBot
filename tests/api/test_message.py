from typing import List
import pytest

from origamibot.api.message_api import MessageAPI
from origamibot.types import Message, Chat, MessageId

from .. import token, private_cid, image_file


sent_messages: List[Message] = []


@pytest.fixture
def api(token):
    return MessageAPI(token)


@pytest.mark.asyncio
async def test_send_message(api: MessageAPI, private_cid):
    m = await api.send_message(
        chat_id=private_cid,
        text='Test message from MessageAPI'
    )
    assert isinstance(m, Message)
    assert isinstance(m.chat, Chat)
    sent_messages.append(m)


@pytest.mark.asyncio
@pytest.mark.order(after='test_send_message')
async def test_update_message_text(api: MessageAPI):
    for m in sent_messages:
        if not m.text:
            continue
        assert await api.edit_message_text('Edited text', chat_id=m.chat.id, message_id=m.message_id)


@pytest.mark.asyncio
@pytest.mark.order(before='test_update_message_caption')
async def test_send_photo(api: MessageAPI, private_cid, image_file):
    m = await api.send_photo(
        chat_id=private_cid,
        photo=image_file,
        caption='Test image from MessageAPI'
    )
    assert isinstance(m, Message)
    sent_messages.append(m)
    

@pytest.mark.asyncio
@pytest.mark.order(after='test_update_message_text')
async def test_update_message_caption(api: MessageAPI):
    for m in sent_messages:
        if not m.caption:
            continue
        assert await api.edit_message_caption('New Caption', chat_id=m.chat.id, message_id=m.message_id)


@pytest.mark.asyncio
@pytest.mark.order(after='test_send_message')
async def test_forward_message(api: MessageAPI):
    if not sent_messages:
        pytest.skip('No messages to forward')
    m = sent_messages[0]
    new_msg = await api.forward_message(m.chat.id, m.chat.id, m.message_id)
    assert isinstance(new_msg, Message)
    sent_messages.append(new_msg)


@pytest.mark.asyncio
@pytest.mark.order(after='test_send_message')
async def test_copy_message(api: MessageAPI):
    if not sent_messages:
        pytest.skip('No messages to copy')
    m = sent_messages[0]
    new_msg_id = await api.copy_message(m.chat.id, m.chat.id, m.message_id)
    assert isinstance(new_msg_id, MessageId)


@pytest.mark.asyncio
@pytest.mark.order('last')
async def test_delete_message(api: MessageAPI):
    for m in sent_messages:
        assert await api.delete_message(m.chat.id, m.message_id)
