from typing import Union

from .base import Field, InputMedia
from .input_file import InputFile


class InputMediaAudio(InputMedia):

    thumb = Field()
    caption = Field()
    parse_mode = Field()
    duration = Field()
    performer = Field()
    title = Field()

    def __init__(self,
                 media: str,
                 thumb: Union[str, InputFile],
                 caption: str = None,
                 parse_mode: str = None,
                 duration: int = None,
                 performer: str = None,
                 title: str = None
                 ):
        super().__init__('audio', media)

        self.thumb = \
            Field(thumb, [str, InputFile])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.duration = \
            Field(duration, [int])

        self.performer = \
            Field(performer, [str])

        self.title = \
            Field(title, [str])
