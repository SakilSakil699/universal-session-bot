
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Engines package — multi-library Telegram login.
"""
from .base import BaseEngine, LoginResult
from .telethon_engine import TelethonEngine
from .pyro_engine import PyrogramEngine

# Optional engines (conditional import)
try:
    from .ferogram_engine import FerogramEngine
    _FEROGRAM_AVAILABLE = True
except ImportError:
    FerogramEngine = None
    _FEROGRAM_AVAILABLE = False

__version__ = "1.0.0"
__author__ = "Sakil"
__author_username__ = "@YO_UR_OFFICIAL_CRUSH"
__author_url__ = "https://t.me/YO_UR_OFFICIAL_CRUSH"
__github__ = "https://github.com/SakilSakil699"

__all__ = [
    "BaseEngine",
    "LoginResult",
    "TelethonEngine",
    "PyrogramEngine",
    "FerogramEngine",
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
]
