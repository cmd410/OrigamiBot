from flowerfield import Field, ListField, OptionalField

from ._base import TelegramType


class InputFile:
    # TODO InputFile
    pass


class InputMedia(TelegramType, root=True):
    type             = Field(str)
    media            = Field(str)
    caption          = OptionalField(str)
    parse_mode       = OptionalField(str)
    caption_entities = ListField('MessageEntity')


class InputMediaPhoto(InputMedia):
    # No unique fields here...
    pass


class InputMediaVideo(InputMedia):
    thumb              = OptionalField(str, 'InputFile')
    width              = OptionalField(int)
    height             = OptionalField(int)
    duration           = OptionalField(int)
    supports_streaming = OptionalField(bool)


class InputMediaAnimation(InputMedia):
    thumb    = OptionalField(str, InputFile)
    width    = OptionalField(int)
    height   = OptionalField(int)
    duration = OptionalField(int)


class InputMediaAudio(InputMedia):
    thumb     = OptionalField(str, InputFile)
    duration  = OptionalField(int)
    performer = OptionalField(str)
    title     = OptionalField(str)


class InputMediaDocument(InputMedia):
    thumb = OptionalField(str, InputFile)
    disable_content_type_detection = OptionalField(bool)
