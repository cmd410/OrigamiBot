from origamibot.types.update import Update
import pytest

from origamibot.api import UpdateAPI
from origamibot.types import Update

from .. import token, webhook


@pytest.fixture
def api(token):
    return UpdateAPI(token=token)


@pytest.mark.asyncio
async def test_update_api(api: UpdateAPI):
    """Test UpdateAPI class
    """
    async for upd in api.get_updates(timeout=0):
        assert isinstance(upd, Update)



@pytest.mark.asyncio
async def test_webhooks(api: UpdateAPI, webhook: str):
    whi = await api.get_webhook_info()
    if whi.url:
        assert await api.delete_webhook()
    
    assert await api.set_webhook(url=webhook)
    
    whi = await api.get_webhook_info()
    
    assert whi.url == webhook
    assert await api.delete_webhook()
