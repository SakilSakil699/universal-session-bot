"""
Core package — session conversion, parsing, universal models.
"""
from .universal_session import UniversalSession
from .converters import SessionConverter
from .session_parser import SessionParser
from .session_utils import SessionUtils
from .exceptions import (
    SessionBotError,
    InvalidSessionError,
    ConversionError,
    LoginError,
    RateLimitError,
    EncryptionError,
)

__all__ = [
    "UniversalSession",
    "SessionConverter",
    "SessionParser",
    "SessionUtils",
    "SessionBotError",
    "InvalidSessionError",
    "ConversionError",
    "LoginError",
    "RateLimitError",
    "EncryptionError",
]
