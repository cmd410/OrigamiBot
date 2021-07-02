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
@pytest.mark.order('last')
async def test_delete_message(api: MessageAPI):
    for m in sent_messages:
        assert await api.delete_message(m.chat.id, m.message_id)
