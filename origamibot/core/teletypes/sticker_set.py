from typing import Optional, List
from .sticker import Sticker
from .photo_size import PhotoSize
from .base import TelegramStructure, Field, ListField


class StickerSet(TelegramStructure):
  name = Field()
  title = Field()
  is_animated = Field()
  is_video = Field()
  contains_masks = Field()
  stickers = ListField()
  thumb = Field()

  def __init__(self,
              name: str,
              title: str,
              is_animated: bool,
              is_video: bool,
              contains_masks: bool,
              stickers: List[Sticker],
              thumb: Optional[PhotoSize]
              ):
    self.name = Field(name, [str])
    self.title = Field(title, [str])
    self.is_animated = Field(is_animated, [bool])
    self.is_video = Field(is_video, [bool])
    self.contains_masks = Field(contains_masks, [bool])
    self.stickers = ListField(stickers, [Sticker])
    self.thumb = Field(thumb, [PhotoSize])
