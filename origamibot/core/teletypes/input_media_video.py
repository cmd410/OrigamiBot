from typing import Union

from .base import Field, InputMedia
from .input_file import InputFile


class InputMediaVideo(InputMedia):

    thumb = Field()
    caption = Field()
    parse_mode = Field()
    width = Field()
    height = Field()
    duration = Field()
    supports_streaming = Field()

    def __init__(self,
                 media: str,
                 thumb: Union[str, InputFile],
                 caption: str = None,
                 parse_mode: str = None,
                 width: int = None,
                 height: int = None,
                 duration: int = None,
                 supports_streaming: bool = None
                 ):
        super().__init__('video', media)

        self.thumb = \
            Field(thumb, [str, InputFile])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])

        self.width = \
            Field(width, [int])

        self.height = \
            Field(height, [int])

        self.duration = \
            Field(duration, [int])

        self.supports_streaming = \
            Field(supports_streaming, [bool])
