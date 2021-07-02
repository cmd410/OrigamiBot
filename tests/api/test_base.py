import pytest

from origamibot.api._base import APIBase
from origamibot.types import User

from .. import token


@pytest.fixture
def api(token):
    return APIBase(token)


@pytest.mark.asyncio
async def test_get_me(api: APIBase):
    me = await api.get_me()
    assert isinstance(me, User)
