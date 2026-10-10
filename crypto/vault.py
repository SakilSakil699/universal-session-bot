
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

AES-256-GCM encrypted vault for session storage.
Zero-knowledge: even DB leak = no plaintext leak.
"""
import os
import json
import struct

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .kdf import KeyDerivation
from .key_utils import KeyUtils
from core.universal_session import UniversalSession
from core.exceptions import EncryptionError


class SessionVault:
    """
    Encrypted storage for UniversalSession objects.
    
    Format on disk:
        [1B version][16B salt][12B nonce][ciphertext + 16B tag]
        → URL-safe base64
    """
    
    VERSION = 0x01
    
    def __init__(self, master_key_hex: str):
        KeyUtils.validate_master_key(master_key_hex)
        self._master_key = bytes.fromhex(master_key_hex)
    
    # ═══════════════════════════════════════════════
    #  Low-level encrypt / decrypt
    # ═══════════════════════════════════════════════
    
    def encrypt_bytes(self, plaintext: bytes) -> bytes:
        """Encrypt bytes → version + salt + nonce + ciphertext."""
        try:
            salt = KeyDerivation.generate_salt()
            nonce = KeyUtils.generate_nonce()
            key = KeyDerivation.derive_key(self._master_key.hex(), salt)
            aes = AESGCM(key)
            ct = aes.encrypt(nonce, plaintext, None)
            return struct.pack(">B", self.VERSION) + salt + nonce + ct
        except Exception as e:
            raise EncryptionError(f"Encrypt failed: {e}")
    
    def decrypt_bytes(self, blob: bytes) -> bytes:
        """Decrypt blob produced by encrypt_bytes()."""
        try:
            if len(blob) < 1 + 16 + 12 + 16:
                raise EncryptionError("Blob too short")
            
            version = blob[0]
            if version != self.VERSION:
                raise EncryptionError(f"Unknown version: {version}")
            
            salt = blob[1:17]
            nonce = blob[17:29]
            ct = blob[29:]
            
            key = KeyDerivation.derive_key(self._master_key.hex(), salt)
            aes = AESGCM(key)
            return aes.decrypt(nonce, ct, None)
        except EncryptionError:
            raise
        except Exception as e:
            raise EncryptionError(f"Decrypt failed: {e}")
    
    # ═══════════════════════════════════════════════
    #  Session-level encrypt / decrypt
    # ═══════════════════════════════════════════════
    
    def encrypt_session(self, s: UniversalSession) -> str:
        """Encrypt UniversalSession → base64 string."""
        payload = json.dumps(s.to_dict(), default=str).encode()
        blob = self.encrypt_bytes(payload)
        return KeyUtils.b64_encode(blob)
    
    def decrypt_session(self, encoded: str) -> UniversalSession:
        """Decrypt base64 string → UniversalSession."""
        try:
            blob = KeyUtils.b64_decode(encoded)
            payload = self.decrypt_bytes(blob)
            data = json.loads(payload.decode())
            return UniversalSession.from_dict(data)
        except EncryptionError:
            raise
        except Exception as e:
            raise EncryptionError(f"Session decrypt failed: {e}")
    
    # ═══════════════════════════════════════════════
    #  Text encrypt / decrypt
    # ═══════════════════════════════════════════════
    
    def encrypt_text(self, text: str) -> str:
        blob = self.encrypt_bytes(text.encode())
        return KeyUtils.b64_encode(blob)
    
    def decrypt_text(self, encoded: str) -> str:
        blob = KeyUtils.b64_decode(encoded)
        return self.decrypt_bytes(blob).decode()
