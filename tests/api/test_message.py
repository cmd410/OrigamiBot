import pytest

from origamibot.api.message_api import MessageAPI
from origamibot.types import Message

from .. import token, private_cid


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
    
