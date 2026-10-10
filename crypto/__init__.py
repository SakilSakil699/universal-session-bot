
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Crypto package — encryption, key derivation, hashing.
"""
from .vault import SessionVault
from .kdf import KeyDerivation
from .key_utils import KeyUtils

__version__ = "1.0.0"
__author__ = "Sakil"
__author_username__ = "@YO_UR_OFFICIAL_CRUSH"
__author_url__ = "https://t.me/YO_UR_OFFICIAL_CRUSH"
__github__ = "https://github.com/SakilSakil699"

__all__ = [
    "SessionVault",
    "KeyDerivation",
    "KeyUtils",
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
]
