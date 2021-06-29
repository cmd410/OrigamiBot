from . import bot, token, private_cid


def test_send_message(bot, private_cid):
    message = bot.send_message(chat_id=private_cid, text='Test message')
    assert message
