from typing import Union

from .base import Field, InputMedia
from .input_file import InputFile


class InputMediaDocument(InputMedia):

    thumb = Field()
    caption = Field()
    parse_mode = Field()

    def __init__(self,
                 media: str,
                 thumb: Union[str, InputFile] = None,
                 caption: str = None,
                 parse_mode: str = None
                 ):
        super().__init__('document', media)

        self.thumb = \
            Field(thumb, [str, InputFile])

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])
