import pytest

from origamibot.core.teletypes import BotCommand, BotCommandScopeDefault

from . import bot, token, private_cid


@pytest.mark.run('first')
def test_set_my_commands(bot):
    assert bot.set_my_commands([
        BotCommand('/start', 'just a start command')
    ],
    scope=BotCommandScopeDefault(),
    )


@pytest.mark.run('last')
def test_delete_my_commands(bot):
    assert bot.delete_my_commands(
        scope=BotCommandScopeDefault()
    )
