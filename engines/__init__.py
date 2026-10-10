"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Engines package — multi-library Telegram login.
Exports: Telethon, Pyrogram, Ferogram (optional) engines.
"""
from .base import BaseEngine, LoginResult
from .telethon_engine import TelethonEngine
from .pyro_engine import PyrogramEngine

# ── Optional: Ferogram (Rust core, experimental) ──
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
__repo__ = "https://github.com/SakilSakil699/universal-session-bot"


def get_engine(name: str, api_id: int, api_hash: str, proxy: dict = None):
    """
    Factory: get engine instance by name.

    Supported: "telethon", "pyrogram", "ferogram"
    """
    engines = {
        "telethon": TelethonEngine,
        "pyrogram": PyrogramEngine,
    }

    if _FEROGRAM_AVAILABLE:
        engines["ferogram"] = FerogramEngine

    cls = engines.get(name.lower())
    if not cls:
        raise ValueError(
            f"Unknown engine: {name}. "
            f"Available: {', '.join(engines.keys())}"
        )

    return cls(api_id=api_id, api_hash=api_hash, proxy=proxy)


def available_engines() -> list:
    """List of engine names currently available."""
    names = ["telethon", "pyrogram"]
    if _FEROGRAM_AVAILABLE:
        names.append("ferogram")
    return names


__all__ = [
    # Base
    "BaseEngine",
    "LoginResult",
    # Engines
    "TelethonEngine",
    "PyrogramEngine",
    "FerogramEngine",
    # Helpers
    "get_engine",
    "available_engines",
    # Meta
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
    "__repo__",
]
