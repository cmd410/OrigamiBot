from ._base import TelegramObject


class MessageId(TelegramObject):
    """This object represents a unique message identifier.
    """
    message_id: int
