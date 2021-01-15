from flowerfield import Scheme


class TelegramType(Scheme, root=True):
    _bot = None  # Bot that owns this object
