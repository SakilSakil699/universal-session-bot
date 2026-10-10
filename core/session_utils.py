
"""
Session utility helpers.
Extract auth_key, dc_id, user_id from any session object.
Validation, hashing, and metadata helpers.
"""
import hashlib
import hmac
import struct
from typing import Optional, Union
from datetime import datetime

from .universal_session import UniversalSession
from .exceptions import InvalidSessionError


class SessionUtils:
    """
    Utility functions for session manipulation.
    Stateless — all static methods.
    """
    
    # ═══════════════════════════════════════════════
    #  Auth Key Validation
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def validate_auth_key(auth_key: bytes) -> bool:
        """
        Validate auth_key is exactly 256 bytes and not all zeros.
        """
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
        """DC ID must be 1-5."""
        if dc_id not in (1, 2, 3, 4, 5):
            raise InvalidSessionError(f"Invalid dc_id: {dc_id}. Must be 1-5.")
        return True
    
    @staticmethod
    def validate_session(s: UniversalSession) -> bool:
        """Full validation of UniversalSession object."""
        SessionUtils.validate_auth_key(s.auth_key)
        SessionUtils.validate_dc_id(s.dc_id)
        if s.user_id < 0:
            raise InvalidSessionError("user_id cannot be negative")
        return True
    
    # ═══════════════════════════════════════════════
    #  Auth Key Fingerprint (for dedup/logging)
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def auth_key_fingerprint(auth_key: bytes) -> str:
        """
        Short SHA-256 fingerprint of auth_key.
        Safe to log — cannot be reversed.
        """
        return hashlib.sha256(auth_key).hexdigest()[:16]
    
    @staticmethod
    def session_hash(s: UniversalSession) -> str:
        """
        Unique hash of a session for dedup detection.
        Same session = same hash.
        """
        payload = (
            s.auth_key
            + struct.pack(">B", s.dc_id)
            + struct.pack(">Q", s.user_id)
        )
        return hashlib.sha256(payload).hexdigest()
    
    # ═══════════════════════════════════════════════
    #  Extract from Telegram Client
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def extract_from_telethon(client) -> dict:
        """
        Extract auth data from a connected Telethon client.
        Returns dict with auth_key, dc_id, user_id, etc.
        """
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
        """
        Extract auth data from a connected Pyrogram client.
        """
        try:
            session = client.storage
            auth_key = session.auth_key if hasattr(session, "auth_key") else b""
            
            me = client.me
            return {
                "auth_key": bytes(auth_key) if auth_key else b"",
                "dc_id": getattr(session, "dc_id", 4),
                "user_id": me.id if me else 0,
                "is_bot": me.is_bot if me else False,
                "phone": getattr(me, "phone_number", None),
                "first_name": getattr(me, "first_name", None),
                "last_name": getattr(me, "last_name", None),
                "username": getattr(me, "username", None),
            }
        except Exception as e:
            raise InvalidSessionError(f"Pyrogram extract failed: {e}")
    
    # ═══════════════════════════════════════════════
    #  Metadata Helpers
    # ═══════════════════════════════════════════════
    
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
            lines.append("🤖 This is a Bot account")
        return "\n".join(lines)
    
    @staticmethod
    def mask_session_string(s: str, show: int = 20) -> str:
        """
        Mask session string for safe display.
        Shows first & last N chars only.
        """
        if len(s) <= show * 2:
            return s[:show] + "***"
        return f"{s[:show]}...{s[-show:]}"
    
    @staticmethod
    def bytes_to_human(b: int) -> str:
        """Format bytes to human-readable (KB/MB)."""
        for unit in ("B", "KB", "MB", "GB"):
            if b < 1024:
                return f"{b:.2f} {unit}"
            b /= 1024
        return f"{b:.2f} TB"
    
    # ═══════════════════════════════════════════════
    #  Clone & Compare
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def clone(s: UniversalSession) -> UniversalSession:
        """Deep clone a session object."""
        return UniversalSession(
            auth_key=bytes(s.auth_key),
            dc_id=s.dc_id,
            user_id=s.user_id,
            api_id=s.api_id,
            api_hash=s.api_hash,
            is_bot=s.is_bot,
            test_mode=s.test_mode,
            phone=s.phone,
            first_name=s.first_name,
            last_name=s.last_name,
            username=s.username,
        )
    
    @staticmethod
    def is_same_session(a: UniversalSession, b: UniversalSession) -> bool:
        """Check if two sessions point to same account+dc."""
        return (
            hmac.compare_digest(a.auth_key, b.auth_key)
            and a.dc_id == b.dc_id
        )
    
    # ═══════════════════════════════════════════════
    #  Estimate Session Age
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def age_string(created_at: datetime) -> str:
        """Human-friendly age like '2 hours ago'."""
        delta = datetime.utcnow() - created_at
        secs = int(delta.total_seconds())
        
        if secs < 60:
            return f"{secs}s ago"
        if secs < 3600:
            return f"{secs // 60}m ago"
        if secs < 86400:
            return f"{secs // 3600}h ago"
        return f"{secs // 86400}d ago"
