"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Core package — session conversion, parsing, universal models.

Exports:
    - UniversalSession : Common session dataclass
    - SessionConverter : Format ↔ Format converter
    - SessionParser    : Auto-detect & parse any session format
    - SessionUtils     : Validation, fingerprint, extract helpers
    - Exceptions       : Custom error hierarchy
"""

# ── Models ───────────────────────────────────────
from .universal_session import UniversalSession

# ── Converters ───────────────────────────────────
from .converters import SessionConverter

# ── Parsers ──────────────────────────────────────
from .session_parser import SessionParser

# ── Utils ────────────────────────────────────────
from .session_utils import SessionUtils

# ── Exceptions ───────────────────────────────────
from .exceptions import (
    SessionBotError,
    InvalidSessionError,
    ConversionError,
    LoginError,
    RateLimitError,
    EncryptionError,
)


__version__ = "1.0.0"
__author__ = "Sakil"
__author_username__ = "@YO_UR_OFFICIAL_CRUSH"
__author_url__ = "https://t.me/YO_UR_OFFICIAL_CRUSH"
__github__ = "https://github.com/SakilSakil699"
__repo__ = "https://github.com/SakilSakil699/universal-session-bot"


__all__ = [
    # Models
    "UniversalSession",
    # Converters
    "SessionConverter",
    # Parsers
    "SessionParser",
    # Utils
    "SessionUtils",
    # Exceptions
    "SessionBotError",
    "InvalidSessionError",
    "ConversionError",
    "LoginError",
    "RateLimitError",
    "EncryptionError",
    # Meta
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
    "__repo__",
]
