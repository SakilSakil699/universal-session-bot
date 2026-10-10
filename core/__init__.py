
"""
Core package — session conversion, parsing, universal models.
"""
from .universal_session import UniversalSession
from .converters import SessionConverter
from .session_parser import SessionParser
from .exceptions import (
    SessionBotError,
    InvalidSessionError,
    ConversionError,
    LoginError,
    RateLimitError,
)

__all__ = [
    "UniversalSession",
    "SessionConverter",
    "SessionParser",
    "SessionBotError",
    "InvalidSessionError",
    "ConversionError",
    "LoginError",
    "RateLimitError",
]
