from .base import TelegramStructure, Field


class MaskPosition(TelegramStructure):

    point = Field()
    x_shift = Field()
    y_shift = Field()
    scale = Field()

    def __init__(self,
                 point: str,
                 x_shift: float,
                 y_shift: float,
                 scale: float
                 ):
        self.point = \
            Field(point, [str])

        self.x_shift = \
            Field(x_shift, [float])

        self.y_shift = \
            Field(y_shift, [float])

        self.scale = \
            Field(scale, [float])
