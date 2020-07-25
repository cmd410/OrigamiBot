



![](https://media.githubusercontent.com/media/cmd410/OrigamiBot/master/imgs/logo.png)

Library for creating bots for telegram with [Python](https://www.python.org/). 

**OrigamiBot** aims to make development of Telegram bots as easy and flexible as possible.

![Upload Python Package](https://github.com/cmd410/OrigamiBot/workflows/Upload%20Python%20Package/badge.svg)

## Installation

Origamibot is published in [PyPI](https://pypi.org/project/origamibot/), so it can be installed with one simple command:

```
pip install origamibot
```

## Basic concepts

**OrigamiBot** class is thing that will get updates form the server and dispatch them to your **command holders** and **event listeners**.

- **Command Holder** is a custom class that you create that exposes its methods as commands for bot
  command holder can be attached to bot using `bot.add_commands(your_command_holder_class())`
- **Event listener** is a class that inherits from `origamibot.util.Listener` and performs some actions on certain events(when its `on_<something>` methods are called from **OrigamiBot**). Event listener can be added to bot with `bot.add_listener(your_listener_object)` 

## Usage example

Here goes a simple example of a bot:

```python
from sys import argv
from time import sleep

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener


class BotsCommands:
    def __init__(self, bot: Bot):  # Can initialize however you like
        self.bot = bot

    def start(self, message):   # /start command
        self.bot.send_message(
            message.chat.id,
            'Hello user!\nThis is an example bot.')

    def echo(self, message, value: str):  # /echo [value: str] command
        self.bot.send_message(
            message.chat.id,
            value
            )

    def add(self, message, a: float, b: float):  # /add [a: float] [b: float]
        self.bot.send_message(
            message.chat.id,
            str(a + b)
            )

    def _not_a_command(self):   # This method not considered a command
        print('I am not a command')


class MessageListener(Listener):  # Event listener must inherit Listener
    def __init__(self, bot):
        self.bot = bot
        self.m_count = 0

    def on_message(self, message):   # called on every message
        self.m_count += 1
        print(f'Total messages: {self.m_count}')

    def on_command_failure(self, message, err=None):  # When command fails
        if err is None:
            self.bot.send_message(message.chat.id,
                                  'Command failed to bind arguments!')
        else:
            self.bot.send_message(message.chat.id,
                                  'Error in command:\n{err}')


if __name__ == '__main__':
    token = (argv[1] if len(argv) > 1 else input('Enter bot token: '))
    bot = Bot(token)   # Create instance of OrigamiBot class

    # Add an event listener
    bot.add_listener(MessageListener(bot))

    # Add a command holder
    bot.add_commands(BotsCommands(bot))

    # We can add as many command holders
    # and event listeners as we like

    bot.start()   # start bot's threads
    while True:
        sleep(1)
        # Can also do some useful work i main thread
        # Like autoposting to channels for example
```

Commands are added as methods of an object(be it class or instance of it), if their names don't start with `_` which makes it possible to also contain some utility functions inside command container. 

For the command to be called two conditions must be met:

1. command name must match with method name
2. command's arguments must match signature of a method

Method signature supports any number of arguments with simple typing(`str`, `int`, `float`, `bool`) or without a typing(in this case all arguments are strings by default), as well as variable number of arguments `*args`. More complex types(as lists, tuples, custom object classes) are not supported, as bot does not know how to parse them, and I don't want to enforce my own parsing algorithm, but bot will still attempt to convert it like `cls(argument)`, but a correct result is not guaranteed.

> **Boolean** values are considered True if their string representation is in `{'True', 'true', '1'}`, and False if in `{'False', 'false', '0'}`

