import pytest

from origamibot.core.client import TelegramClient, method_var, token_var

from . import token, private_cid, image_file


@pytest.fixture
def client():
    return TelegramClient()


@pytest.mark.asyncio
async def test_client_get_me(client, token):
    await client.arequest(token, 'getMe')


@pytest.mark.asyncio
async def test_client_send_message(client, token, private_cid):
    await client.arequest(
        token,
        'sendMessage',
        data={
            'chat_id': private_cid,
            'text': 'Test message from client'
        }
    )


@pytest.mark.asyncio
async def test_client_send_photo(client, token, private_cid, image_file):
    print(await client.arequest(
        token,
        'sendPhoto',
        data={
            'chat_id': private_cid,
            'caption': 'Test photo from client'
        },
        files={
            'photo': image_file
        }
    ))
