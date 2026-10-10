"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Session utility helpers — validation, fingerprint, extract.
"""
import hashlib
import hmac
import struct
from datetime import datetime

from .universal_session import UniversalSession
from .exceptions import InvalidSessionError


class SessionUtils:
    """Utility functions for session manipulation. Stateless."""
    
    # ── Validation ───────────────────────────────
    @staticmethod
    def validate_auth_key(auth_key: bytes) -> bool:
        if not isinstance(auth_key, bytes):
            raise InvalidSessionError("auth_key must be bytes")
        if len(auth_key) != 256:
            raise InvalidSessionError(
                f"auth_key must be 256 bytes, got {len(auth_key)}"
            )
        if auth_key == b"\x00" * 256:
            raise InvalidSessionError("auth_key cannot be all zeros")
        return True
    
    @staticmethod
    def validate_dc_id(dc_id: int) -> bool:
        if dc_id not in (1, 2, 3, 4, 5):
            raise InvalidSessionError(f"Invalid dc_id: {dc_id}. Must be 1-5.")
        return True
    
    @staticmethod
    def validate_session(s: UniversalSession) -> bool:
        SessionUtils.validate_auth_key(s.auth_key)
        SessionUtils.validate_dc_id(s.dc_id)
        if s.user_id < 0:
            raise InvalidSessionError("user_id cannot be negative")
        return True
    
    # ── Fingerprint ──────────────────────────────
    @staticmethod
    def auth_key_fingerprint(auth_key: bytes) -> str:
        """Short SHA-256 fingerprint. Safe to log."""
        return hashlib.sha256(auth_key).hexdigest()[:16]
    
    @staticmethod
    def session_hash(s: UniversalSession) -> str:
        """Unique hash of a session for dedup detection."""
        payload = (
            s.auth_key
            + struct.pack(">B", s.dc_id)
            + struct.pack(">Q", s.user_id)
        )
        return hashlib.sha256(payload).hexdigest()
    
    # ── Extract from clients ─────────────────────
    @staticmethod
    def extract_from_telethon(client) -> dict:
        try:
            session = client.session
            auth_key = session.auth_key.key if hasattr(
                session.auth_key, "key"
            ) else session.auth_key
            return {
                "auth_key": bytes(auth_key) if auth_key else b"",
                "dc_id": session.dc_id,
                "user_id": client.me.id if client.me else 0,
                "is_bot": client.me.bot if client.me else False,
                "phone": getattr(client.me, "phone", None),
                "first_name": getattr(client.me, "first_name", None),
                "last_name": getattr(client.me, "last_name", None),
                "username": getattr(client.me, "username", None),
            }
        except Exception as e:
            raise InvalidSessionError(f"Telethon extract failed: {e}")
    
    @staticmethod
    def extract_from_pyrogram(client) -> dict:
        try:
            storage = client.storage
            auth_key = getattr(storage, "auth_key", b"")
            me = client.me
            return {
                "auth_key": bytes(auth_key) if auth_key else b"",
                "dc_id": getattr(storage, "dc_id", 4),
                "user_id": me.id if me else 0,
                "is_bot": me.is_bot if me else False,
                "phone": getattr(me, "phone_number", None),
                "first_name": getattr(me, "first_name", None),
                "last_name": getattr(me, "last_name", None),
                "username": getattr(me, "username", None),
            }
        except Exception as e:
            raise InvalidSessionError(f"Pyrogram extract failed: {e}")
    
    # ── Metadata helpers ─────────────────────────
    @staticmethod
    def format_user_info(s: UniversalSession) -> str:
        """Human-readable user info string."""
        lines = []
        if s.first_name or s.last_name:
            lines.append(f"👤 Name: {s.full_name}")
        if s.username:
            lines.append(f"🆔 Username: @{s.username}")
        lines.append(f"🔢 User ID: <code>{s.user_id}</code>")
        lines.append(f"🌍 DC {s.dc_id} — {s.dc_location}")
        if s.phone:
            lines.append(f"📱 Phone: <code>{s.phone}</code>")
        if s.is_bot:
            lines.append("🤖 Bot account")
        return "\
