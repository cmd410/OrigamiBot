from .base import TelegramStructure, Field
from .photo_size import PhotoSize


class Animation(TelegramStructure):
    """You can provide an animation for your game so that it looks
    stylish in chats (check out Lumberjack for an example). This
    object represents an animation file to be displayed in the
    message containing a game.

    """

    file_id = Field()
    file_unique_id = Field()
    width = Field()
    height = Field()
    duration = Field()
    thumb = Field()
    file_name = Field()
    mime_type = Field()
    file_size = Field()

    def __init__(self,
                 file_id: str,
                 file_unique_id: str,
                 width: int,
                 height: int,
                 duration: int,
                 thumb: PhotoSize = None,
                 file_name: str = None,
                 mime_type: str = None,
                 file_size: int = None,
                 ):
        self.file_id = \
            Field(file_id, [str])

        self.file_unique_id = \
            Field(file_unique_id, [str])

        self.width = \
            Field(width, [int])

        self.height = \
            Field(height, [int])

        self.duration = \
            Field(duration, [int])

        self.thumb = \
            Field(thumb, [PhotoSize])

        self.file_name = \
            Field(file_name, [str])

        self.mime_type = \
            Field(mime_type, [str])

        self.file_size = \
            Field(file_size, [int])
