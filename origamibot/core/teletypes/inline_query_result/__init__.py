from .article import InlineQueryResultArticle as Article
from .audio import InlineQueryResultAudio as Audio
from .cached_audio import InlineQueryResultCachedAudio as CachedAudio
from .cached_document import InlineQueryResultCachedDocument as CachedDocument
from .cached_gif import InlineQueryResultCachedGif as CachedGif
from .cached_mpeg4_gif import InlineQueryResultCachedMpeg4Gif as CachedMpeg4Gif
from .cached_sticker import InlineQueryResultCachedSticker as CachedSticker
from .cached_video import InlineQueryResultCachedVideo as CachedVideo
from .cached_voice import InlineQueryResultCachedVoice as CachedVoice
from .contact import InlineQueryResultContact as Contact
from .document import InlineQueryResultDocument as Document
from .game import InlineQueryResultGame as Game
from .gif import InlineQueryResultGif as Gif
from .location import InlineQueryResultLocation as Location
from .mpeg4gif import InlineQueryResultMpeg4Gif as Mpeg4Gif
from .photo import InlineQueryResultPhoto as Photo
from .venue import InlineQueryResultVenue as Venue
from .video import InlineQueryResultVideo as Video
from .voice import InlineQueryResultVoice as Voice

from typing import Union

InlineQueryResult = Union[
    Article,
    Audio,
    CachedAudio,
    CachedDocument,
    CachedGif,
    CachedMpeg4Gif,
    CachedSticker,
    CachedVideo,
    CachedVoice,
    Contact,
    Document,
    Game,
    Gif,
    Location,
    Mpeg4Gif,
    Photo,
    Venue,
    Video,
    Voice
]