from .base import TelegramStructure, Field


class Location(TelegramStructure):
    """This object represents a point on the map.

    """

    longitude = Field()
    latitude = Field()

    def __init__(self,
                 longitude: float,
                 latitude: float,
                 ):
        self.longitude = \
            Field(longitude, [float])

        self.latitude = \
            Field(latitude, [float])
