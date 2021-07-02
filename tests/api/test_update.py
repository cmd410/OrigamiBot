from origamibot.types.update import Update
import pytest

from origamibot.api import UpdateAPI
from origamibot.types import Update

from .. import token, webhook


@pytest.fixture
def update_api(token):
    return UpdateAPI(token=token)


@pytest.mark.asyncio
async def test_update_api(update_api: UpdateAPI):
    """Test UpdateAPI class
    """
    updates = await update_api.get_updates(timeout=0)
    assert isinstance(updates, list)
    assert len(updates) == 0 or all(isinstance(i, Update) for i in updates)



@pytest.mark.asyncio
async def test_webhooks(update_api: UpdateAPI, webhook: str):
    whi = await update_api.get_webhook_info()
    if whi.url:
        assert await update_api.delete_webhook()
    
    assert await update_api.set_webhook(url=webhook)
    
    whi = await update_api.get_webhook_info()
    
    assert whi.url == webhook
    assert await update_api.delete_webhook()
