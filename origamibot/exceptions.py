class OrigamiBaseException(RuntimeError):
    """Base exception for all error raised in this framework
    """

class TelegramAPIError(OrigamiBaseException):
    """Telegram Bot API related errors
    """

class ClientError(OrigamiBaseException):
    """Error occured in the client-server communication.
    
    Usually a network failure.
    """
