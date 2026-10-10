
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Ferogram login engine — Rust core, ultra-fast MTProto.
Experimental. Requires: pip install ferogram
"""
import logging
from typing import Dict

from .base import BaseEngine, LoginResult
from core.universal_session import UniversalSession
from core.session_utils import SessionUtils

log = logging.getLogger(__name__)

# ── Conditional import ───────────────────────────
try:
    from ferogram import Client as FerogramClient
    FEROGRAM_AVAILABLE = True
except ImportError:
    FEROGRAM_AVAILABLE = False
    FerogramClient = None
    log.warning("Ferogram not installed. Install: pip install ferogram")


class FerogramEngine(BaseEngine):
    """
    Ferogram-based login (Rust core).
    Ultra-fast MTProto implementation.
    
    ⚠️ Experimental — Ferogram is in pre-release.
    Use Telethon/Pyrogram for production.
    """
    
    NAME = "ferogram"
    DISPLAY_NAME = "🦀 Ferogram"
    
    def __init__(self, *args, **kwargs):
        if not FEROGRAM_AVAILABLE:
            raise ImportError(
                "Ferogram not installed. Run: pip install ferogram"
            )
        super().__init__(*args, **kwargs)
        self._clients: Dict[str, "FerogramClient"] = {}
    
    def _get_client(self, phone: str) -> "FerogramClient":
        """Get or create Ferogram client for this phone."""
        if phone not in self._clients:
            self._clients[phone] = FerogramClient(
                session=f"ferogram_{phone}",
                api_id=self.api_id,
                api_hash=self.api_hash,
                proxy=self.proxy,
            )
        return self._clients[phone]
    
    async def send_code(self, phone: str) -> LoginResult:
        try:
            client = self._get_client(phone)
            await client.start()
            
            # Ferogram send_code API
            sent = await client.send_code(phone)
            
            log.info(f"Ferogram OTP sent to {phone[:5]}***")
            return LoginResult(
                success=True,
                phone_code_hash=getattr(sent, "phone_code_hash", None),
                needs_code=True,
            )
        except Exception as e:
            log.error(f"Ferogram send_code failed: {e}")
            return self._error(f"❌ {e}")
    
    async def verify_code(
        self, phone: str, code: str, phone_code_hash: str
    ) -> LoginResult:
        try:
            client = self._get_client(phone)
            
            # Ferogram sign_in
            await client.sign_in(
                phone_number=phone,
                phone_code=code,
                phone_code_hash=phone_code_hash,
            )
            
            return await self._extract(client)
        except Exception as e:
            err = str(e).lower()
            if "password" in err or "2fa" in err:
                return LoginResult(success=False, needs_password=True)
            log.error(f"Ferogram verify_code failed: {e}")
            return self._error(f"❌ {e}")
    
    async def verify_password(
        self, phone: str, password: str
    ) -> LoginResult:
        try:
            client = self._get_client(phone)
            await client.check_password(password)
            return await self._extract(client)
        except Exception as e:
            log.error(f"Ferogram 2FA failed: {e}")
            return self._error(f"❌ 2FA failed: {e}")
    
    async def _extract(self, client) -> LoginResult:
        """Extract session from Ferogram client."""
        try:
            me = await client.get_me()
            
            # Ferogram exposes auth_key via session
            session_data = client.session
            auth_key = getattr(session_data, "auth_key", b"")
            dc_id = getattr(session_data, "dc_id", 4)
            
            session = UniversalSession(
                auth_key=bytes(auth_key) if auth_key else b"",
                dc_id=dc_id,
                user_id=me.id,
                api_id=self.api_id,
                api_hash=self.api_hash,
                is_bot=getattr(me, "bot", False),
                phone=getattr(me, "phone", None),
                first_name=getattr(me, "first_name", None),
                last_name=getattr(me, "last_name", None),
                username=getattr(me, "username", None),
            )
            
            log.info(f"Ferogram login success: user_id={me.id}")
            return LoginResult(success=True, session=session)
        except Exception as e:
            log.error(f"Ferogram extract failed: {e}")
            return self._error(f"Extract failed: {e}")
    
    async def cleanup(self) -> None:
        for phone, client in list(self._clients.items()):
            try:
                if hasattr(client, "disconnect"):
                    await client.disconnect()
            except Exception:
                pass
            finally:
                self._clients.pop(phone, None)
