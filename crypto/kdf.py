
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Argon2id key derivation.
Converts password → 32-byte encryption key.
"""
import os
from argon2.low_level import hash_secret_raw, Type

from core.exceptions import EncryptionError
from config.constants import Emojis


class KeyDerivation:
    """
    Argon2id KDF — memory-hard, GPU-resistant.
    Recommended by OWASP 2024.
    """
    
    # ── OWASP recommended params ─────────────────
    TIME_COST = 4          # iterations
    MEMORY_COST = 65536    # 64 MB
    PARALLELISM = 4        # threads
    HASH_LEN = 32          # 32 bytes = 256 bits
    SALT_LEN = 16          # 128-bit salt
    
    @classmethod
    def derive_key(cls, password: str, salt: bytes) -> bytes:
        """Derive 256-bit key from password + salt (deterministic)."""
        if not password or len(password) < 8:
            raise EncryptionError(
                f"{Emojis.WARN} Password must be at least 8 chars"
            )
        if len(salt) != cls.SALT_LEN:
            raise EncryptionError(f"Salt must be {cls.SALT_LEN} bytes")
        
        try:
            return hash_secret_raw(
                secret=password.encode("utf-8"),
                salt=salt,
                time_cost=cls.TIME_COST,
                memory_cost=cls.MEMORY_COST,
                parallelism=cls.PARALLELISM,
                hash_len=cls.HASH_LEN,
                type=Type.ID,
            )
        except Exception as e:
            raise EncryptionError(f"KDF failed: {e}")
    
    @staticmethod
    def generate_salt() -> bytes:
        """Cryptographically secure random salt."""
        return os.urandom(KeyDerivation.SALT_LEN)
    
    @classmethod
    def derive_with_new_salt(cls, password: str) -> tuple[bytes, bytes]:
        """Generate new salt + derive key. Returns (key, salt)."""
        salt = cls.generate_salt()
        key = cls.derive_key(password, salt)
        return key, salt
