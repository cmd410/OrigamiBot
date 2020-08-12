from .base import TelegramStructure, Field
from .location import Location


class Venue(TelegramStructure):
    """This object represents a venue.

    """

    location = Field()
    title = Field()
    address = Field()
    foursquare_id = Field()

    def __init__(self,
                 location: Location,
                 title: str,
                 address: str,
                 foursquare_id: str = None,
                 ):
        self.location = \
            Field(location, [Location])

        self.title = \
            Field(title, [str])

        self.address = \
            Field(address, [str])

        self.foursquare_id = \
            Field(foursquare_id, [str])
