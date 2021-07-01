from origamibot.types.update import Update
import pytest

from origamibot.api import UpdateAPI
from origamibot.types import Update

from . import token


@pytest.mark.asyncio
async def test_update_api(token):
    """Test UpdateAPI class
    """
    
    upd_api = UpdateAPI(token=token)
    updates = await upd_api.get_updates(timeout=0)
    
    assert isinstance(updates, list)
    assert len(updates) == 0 or all(isinstance(i, Update) for i in updates)

    wh_info = await upd_api.get_webhook_info()
    assert wh_info.url == ''
