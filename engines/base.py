
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Abstract base for all login engines.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from core.universal_session import UniversalSession


@dataclass
class LoginResult:
    """
    Result of a login attempt.
    If needs_password=True, session is None and user must submit 2FA.
    """
    success: bool
    session: Optional[UniversalSession] = None
    phone_code_hash: Optional[str] = None
    needs_password: bool = False
    needs_code: bool = False
    error: Optional[str] = None


class BaseEngine(ABC):
    """
    Abstract login engine.
    All engines (Telethon, Pyrogram, Ferogram) implement this.
    """
    
    NAME: str = "base"
    DISPLAY_NAME: str = "Base Engine"
    
    def __init__(self, api_id: int, api_hash: str, proxy: dict = None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.proxy = proxy
    
    # ── Abstract methods ─────────────────────────
    
    @abstractmethod
    async def send_code(self, phone: str) -> LoginResult:
        """Send OTP to phone. Returns phone_code_hash."""
        ...
    
    @abstractmethod
    async def verify_code(
        self, phone: str, code: str, phone_code_hash: str
    ) -> LoginResult:
        """Verify OTP. May return needs_password=True."""
        ...
    
    @abstractmethod
    async def verify_password(
        self, phone: str, password: str
    ) -> LoginResult:
        """Verify 2FA password."""
        ...
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup temp session and clients."""
        ...
    
    # ── Shared helpers ───────────────────────────
    
    def _error(self, msg: str) -> LoginResult:
        return LoginResult(success=False, error=msg)
