
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

FastAPI dashboard — REST + WebSocket live stats.
"""
from .app import app, create_app

__version__ = "1.0.0"
__author__ = "Sakil"
__author_username__ = "@YO_UR_OFFICIAL_CRUSH"
__author_url__ = "https://t.me/YO_UR_OFFICIAL_CRUSH"
__github__ = "https://github.com/SakilSakil699"
__repo__ = "https://github.com/SakilSakil699/universal-session-bot"

__all__ = [
    "app",
    "create_app",
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
    "__repo__",
]
