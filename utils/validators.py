
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Input validators — phone, OTP, session strings, usernames.
"""
import re
from typing import Optional


class Validators:
    """Stateless input validators."""
    
    # ── Phone number ─────────────────────────────
    PHONE_REGEX = re.compile(r"^\+\d{8,15}$")
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Validate international phone format.
        Must start with +, 8-15 digits total.
        """
        if not phone or not isinstance(phone, str):
            return False
        return bool(Validators.PHONE_REGEX.match(phone.strip()))
    
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Strip spaces, dashes, parentheses."""
        return re.sub(r"[\s\-\(\)]", "", phone.strip())
    
    # ── OTP ──────────────────────────────────────
    OTP_REGEX = re.compile(r"^\d{4,7}$")
    
    @staticmethod
    def is_valid_otp(otp: str) -> bool:
        """4-7 digit numeric OTP."""
        if not otp:
            return False
        clean = otp.replace(" ", "").strip()
        return bool(Validators.OTP_REGEX.match(clean))
    
    # ── Username ─────────────────────────────────
    USERNAME_REGEX = re.compile(r"^@?[a-zA-Z][a-zA-Z0-9_]{4,31}$")
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Telegram username (5-32 chars, alphanumeric + _)."""
        if not username:
            return False
        return bool(Validators.USERNAME_REGEX.match(username.strip()))
    
    # ── Session string ───────────────────────────
    @staticmethod
    def is_valid_session_string(s: str) -> bool:
        """Loose check — non-empty, no whitespace."""
        if not s or not isinstance(s, str):
            return False
        s = s.strip()
        if len(s) < 100:
            return False
        if any(c.isspace() for c in s):
            return False
        return True
    
    # ── Auth key ─────────────────────────────────
    @staticmethod
    def is_valid_auth_key_hex(hex_str: str) -> bool:
        """Exactly 512 hex chars (256 bytes)."""
        if not hex_str or len(hex_str) != 512:
            return False
        try:
            bytes.fromhex(hex_str)
            return True
        except ValueError:
            return False
    
    # ── DC ID ────────────────────────────────────
    @staticmethod
    def is_valid_dc_id(dc_id) -> bool:
        """DC ID must be 1-5."""
        try:
            return int(dc_id) in (1, 2, 3, 4, 5)
        except (TypeError, ValueError):
            return False
    
    # ── File type ────────────────────────────────
    ALLOWED_EXTENSIONS = {".session", ".json", ".txt", ".zip"}
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """Check if uploaded file extension is allowed."""
        if not filename:
            return False
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        return ext in Validators.ALLOWED_EXTENSIONS
    
    # ── Sanitize for logging ─────────────────────
    @staticmethod
    def mask_phone(phone: str, show: int = 4) -> str:
        """Mask phone for safe logging: +91****3210"""
        if not phone or len(phone) < show + 2:
            return "***"
        return phone[:show] + "*" * (len(phone) - show * 2) + phone[-show:]
