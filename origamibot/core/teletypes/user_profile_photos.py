from typing import List

from .base import TelegramStructure, Field, ListField
from .photo_size import PhotoSize


class UserProfilePhotos(TelegramStructure):
    """This object represent a user's profile pictures.

    """

    total_count = Field()
    photos = Field()

    def __init__(self,
                 total_count: int,
                 photos: List[List[PhotoSize]],
                 ):
        self.total_count = \
            Field(total_count, [int])

        self.photos = \
            ListField(photos, [PhotoSize])
