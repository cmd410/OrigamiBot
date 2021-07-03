from typing import List
import pytest

from origamibot.api.message_api import MessageAPI
from origamibot.types import Message, Chat

from .. import token, private_cid


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
async def test_update_message(api: MessageAPI):
    if not sent_messages:
        pytest.skip('No message were sent, so none left to edit')
    
    for m in sent_messages:
        assert await api.edit_message_text('Edited text', chat_id=m.chat.id, message_id=m.message_id)


@pytest.mark.asyncio
@pytest.mark.order(after='test_update_message')
async def test_delete_message(api: MessageAPI):
    for m in sent_messages:
        assert await api.delete_message(m.chat.id, m.message_id)
