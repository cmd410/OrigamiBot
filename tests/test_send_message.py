from pytest import skip
from . import bot, token, private_cid

try:
  from telegram_text import Bold
  tg_text_present = True
except ImportError:
  tg_text_present = False


def test_send_message(bot, private_cid):
    message = bot.send_message(chat_id=private_cid, text='Test message')
    assert message


def test_telegram_text(bot, private_cid):
  if not tg_text_present: skip("telegram_text is not installed")
  message = bot.send_message(chat_id=private_cid, text=Bold("Bold text message"))
