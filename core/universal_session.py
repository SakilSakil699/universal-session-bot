
"""
UniversalSession — common denominator for all session formats.
Any format can be converted to this, and this to any format.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class UniversalSession:
    """
    Universal session object.
    
    All formats (Pyrogram, Telethon, GramJS, Mtcute, tdata, tgnet)
    can be converted to/from this object.
    """
    # ── Core auth data ──────────────────────────
    auth_key: bytes              # 256-byte MTProto auth key
    dc_id: int                   # 1-5
    user_id: int                 # Telegram user ID
    api_id: int                  # User's API ID
    api_hash: str                # User's API hash
    
    # ── Optional metadata ───────────────────────
    is_bot: bool = False
    test_mode: bool = False
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # ── Derived / helper ────────────────────────
    @property
    def auth_key_hex(self) -> str:
        return self.auth_key.hex()
    
    @property
    def full_name(self) -> str:
        parts = [self.first_name or "", self.last_name or ""]
        return " ".join(p for p in parts if p).strip() or "Unknown"
    
    @property
    def dc_location(self) -> str:
        from config.constants import DC_NAMES
        return DC_NAMES.get(self.dc_id, "Unknown")
    
    def to_dict(self, hide_secrets: bool = False) -> dict:
        """Export to dict. hide_secrets=True for safe logging."""
        d = {
            "dc_id": self.dc_id,
            "user_id": self.user_id,
            "is_bot": self.is_bot,
            "test_mode": self.test_mode,
            "phone": self.phone if not hide_secrets else "***",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }
        if not hide_secrets:
            d["auth_key_hex"] = self.auth_key_hex
            d["api_id"] = self.api_id
            d["api_hash"] = self.api_hash
        return d
    
    def __repr__(self) -> str:
        """Safe repr — no secrets leaked."""
        return (
            f"<UniversalSession user_id={self.user_id} "
            f"dc={self.dc_id} name={self.full_name!r}>"
        )
    
    @classmethod
    def from_dict(cls, d: dict) -> "UniversalSession":
        """Reconstruct from dict (e.g. DB row)."""
        return cls(
            auth_key=bytes.fromhex(d["auth_key_hex"]),
            dc_id=d["dc_id"],
            user_id=d["user_id"],
            api_id=d.get("api_id", 0),
            api_hash=d.get("api_hash", ""),
            is_bot=d.get("is_bot", False),
            test_mode=d.get("test_mode", False),
            phone=d.get("phone"),
            first_name=d.get("first_name"),
            last_name=d.get("last_name"),
            username=d.get("username"),
        )
