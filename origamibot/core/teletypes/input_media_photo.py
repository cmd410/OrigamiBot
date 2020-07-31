from .base import Field, InputMedia


class InputMediaPhoto(InputMedia):

    caption = Field()
    parse_mode = Field()

    def __init__(self,
                 media: str,
                 caption: str,
                 parse_mode: str
                 ):
        super().__init__('photo', media)

        self.caption = \
            Field(caption, [str])

        self.parse_mode = \
            Field(parse_mode, [str])
