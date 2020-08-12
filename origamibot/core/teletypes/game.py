from typing import List

from .base import TelegramStructure, Field, ListField
from .photo_size import PhotoSize
from .animation import Animation
from .message_entity import MessageEntity


class Game(TelegramStructure):
    """This object represents a game. Use BotFather to create and edit
    games, their short names will act as unique identifiers.

    """

    title = Field()
    description = Field()
    photo = Field()
    text = Field()
    text_entities = Field()
    animation = Field()

    def __init__(self,
                 title: str,
                 description: str,
                 photo: List[PhotoSize],
                 text: str = None,
                 text_entities: List[MessageEntity] = None,
                 animation: Animation = None,
                 ):
        self.title = \
            Field(title, [str])

        self.description = \
            Field(description, [str])

        self.photo = \
            ListField(photo, [PhotoSize])

        self.text = \
            Field(text, [str])

        self.text_entities = \
            ListField(text_entities, [MessageEntity])

        self.animation = \
            Field(animation, [Animation])
