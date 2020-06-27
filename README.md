# OrigamiBot - A Pythonic telegram bot API library

> This is WORK IN PROGRESS

Library for creating bots for telegram with [Python](https://www.python.org/). 

## TODO

- implement methods for sending messages, media, etc

## Usage example

Here goes a simple example of a bot:

```python
from sys import argv
from time import sleep

from origamibot import OrigamiBot as Bot

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
        	value)
     
    def add(self, message, a: float, b: float):   # /add [a: float] [b: float] command
        self.bot.send_message(
        	message.chat.id,
            str(a + b)
        )

if __name__ == '__main__':
    token = (argv[1]
             if len(argv) > 1 else 
             input('Enter bot token: '))
    bot = Bot(token)
    bot.add_commands(BotsCommands(bot))
    bot.start()   # start bot's threads
    while True:
        sleep(1)
        # Can also do some useful work i main thread
        # Like autoposting to channels for example
     
```

