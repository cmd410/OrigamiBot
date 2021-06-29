from os import getenv
import importlib as imp

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def token():
    return getenv('TEST_BOT_TOKEN')


@pytest.fixture
def private_cid():
    return int(getenv('TEST_PRIVATE_CHAT'))


@pytest.fixture
def bot(token):
    ob = imp.import_module('origamibot')
    return ob.OrigamiBot(token)
