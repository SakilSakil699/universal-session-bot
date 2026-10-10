
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Database package — async SQLAlchemy models & CRUD.
"""
from .database import Database, db
from .models import Base, User, Session, ActivityLog
from . import crud

__version__ = "1.0.0"
__author__ = "Sakil"
__author_username__ = "@YO_UR_OFFICIAL_CRUSH"
__author_url__ = "https://t.me/YO_UR_OFFICIAL_CRUSH"
__github__ = "https://github.com/SakilSakil699"

__all__ = [
    "Database",
    "db",
    "Base",
    "User",
    "Session",
    "ActivityLog",
    "crud",
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
]
