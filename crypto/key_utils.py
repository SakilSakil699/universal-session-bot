
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Key generation, encoding, and validation helpers.
"""
import os
import secrets
import base64
import hashlib
import hmac

from core.exceptions import EncryptionError


class KeyUtils:
    """Utility helpers for encryption keys."""
    
    KEY_SIZE = 32      # 256-bit
    NONCE_SIZE = 12    # 96-bit for GCM
    TAG_SIZE = 16      # 128-bit auth tag
    
    @staticmethod
    def generate_master_key() -> str:
        """Generate 256-bit master key as hex string (64 chars)."""
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_nonce() -> bytes:
        """Random 96-bit nonce for AES-GCM."""
        return os.urandom(KeyUtils.NONCE_SIZE)
    
    @staticmethod
    def hex_to_bytes(hex_str: str) -> bytes:
        try:
            return bytes.fromhex(hex_str)
        except ValueError as e:
            raise EncryptionError(f"Invalid hex: {e}")
    
    @staticmethod
    def bytes_to_hex(b: bytes) -> str:
        return b.hex()
    
    @staticmethod
    def b64_encode(b: bytes) -> str:
        """URL-safe base64 encode (padding stripped)."""
        return base64.urlsafe_b64encode(b).decode().rstrip("=")
    
    @staticmethod
    def b64_decode(s: str) -> bytes:
        """URL-safe base64 decode (auto padding)."""
        padding = "=" * (-len(s) % 4)
        try:
            return base64.urlsafe_b64decode(s + padding)
        except Exception as e:
            raise EncryptionError(f"Invalid base64: {e}")
    
    @staticmethod
    def constant_time_compare(a: bytes, b: bytes) -> bool:
        """Timing-attack-safe comparison."""
        return hmac.compare_digest(a, b)
    
    @staticmethod
    def sha256(data: bytes) -> bytes:
        return hashlib.sha256(data).digest()
    
    @staticmethod
    def validate_master_key(key: str) -> bool:
        """Ensure ENCRYPTION_KEY is 64 hex chars (32 bytes)."""
        if len(key) != 64:
            raise EncryptionError(
                f"Master key must be 64 hex chars, got {len(key)}"
            )
        try:
            bytes.fromhex(key)
        except ValueError:
            raise EncryptionError("Master key must be valid hex")
        return True
