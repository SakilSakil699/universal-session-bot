"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Custom exceptions for clean error handling.
"""


class SessionBotError(Exception):
    """Base exception for all bot errors."""
    def __init__(self, message: str, user_message: str = None):
        super().__init__(message)
        self.user_message = user_message or message


class InvalidSessionError(SessionBotError):
    """Raised when session string/file is invalid or corrupted."""
    pass


class ConversionError(SessionBotError):
    """Raised when format conversion fails."""
    pass


class LoginError(SessionBotError):
    """Raised when Telegram login fails."""
    pass


class RateLimitError(SessionBotError):
    """Raised when user hits rate limit."""
    pass


class EncryptionError(SessionBotError):
    """Raised when encryption/decryption fails."""
    pass
