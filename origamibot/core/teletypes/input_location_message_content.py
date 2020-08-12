from .base import InputMessageContent, Field


class InputLocationMessageContent(InputMessageContent):

    latitude = Field()
    longitude = Field()
    live_period = Field()

    def __init__(self,
                 latitude: float,
                 longitude: float,
                 live_period: int = None
                 ):
        self.latitude = \
            Field(latitude, [float])

        self.longitude = \
            Field(longitude, [float])

        self.live_period = \
            Field(live_period, [int])
