from .base import Field, InputMessageContent


class InputVenueMessageContent(InputMessageContent):
    """Represents the content of a venue message 
    to be sent as the result of an inline query.
    """

    latitude = Field()
    longitude = Field()
    title = Field()
    address = Field()
    foursquare_id = Field()
    foursquare_type = Field()

    def __init__(self,
                 latitude: float,
                 longitude: float,
                 title: str,
                 address: str,
                 foursquare_id: str = None,
                 foursquare_type: str = None,
                 ):
        self.latitude = \
            Field(latitude, [float])

        self.longitude = \
            Field(longitude, [float])

        self.title = \
            Field(title, [str])

        self.address = \
            Field(address, [str])

        self.foursquare_id = \
            Field(foursquare_id, [str])

        self.foursquare_type = \
            Field(foursquare_type, [str])
