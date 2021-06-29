from pathlib import Path
import json

from origamibot.types.message import Message


def open_sample_json(name: str):
    p = Path(__file__).parent / 'data' / name
    return json.loads(p.read_text())


def test_message():
    d = open_sample_json('message.json')
    m = Message(**d)
    assert m.from_user['id'] == d['from']['id']
