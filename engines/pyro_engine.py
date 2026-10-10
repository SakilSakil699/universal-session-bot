
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Pyrogram login engine — fast, clean API.
"""
import logging
from typing import Dict

from pyrogram import Client
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    FloodWait,
    PhoneNumberInvalid,
)

from .base import BaseEngine, LoginResult
from core.universal_session import UniversalSession
from core.session_utils import SessionUtils

log = logging.getLogger(__name__)


class PyrogramEngine(BaseEngine):
    """Pyrogram-based login."""
    
    NAME = "pyrogram"
    DISPLAY_NAME = "🚀 Pyrogram"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clients: Dict[str, Client] = {}
    
    def _get_client(self, phone: str) -> Client:
        if phone not in self._clients:
            self._clients[phone] = Client(
                name=f"session_{phone}",
                api_id=self.api_id,
                api_hash=self.api_hash,
                in_memory=True,
                proxy=self.proxy,
                device_model="Universal Session Bot",
                system_version="v1.0",
                app_version="v1.0",
            )
        return self._clients[phone]
    
    async def send_code(self, phone: str) -> LoginResult:
        try:
            client = self._get_client(phone)
            await client.connect()
            sent = await client.send_code(phone)
            return LoginResult(
                success=True,
                phone_code_hash=sent.phone_code_hash,
                needs_code=True,
            )
        except PhoneNumberInvalid:
            return self._error("❌ Invalid phone number")
        except FloodWait as e:
            return self._error(f"⏳ Flood wait: {e.value}s")
        except Exception as e:
            log.error(f"Pyro send_code failed: {e}")
            return self._error(f"❌ {e}")
    
    async def verify_code(
        self, phone: str, code: str, phone_code_hash: str
    ) -> LoginResult:
        try:
            client = self._get_client(phone)
            await client.sign_in(
                phone_number=phone,
                phone_code_hash=phone_code_hash,
                phone_code=code,
            )
            return await self._extract(client)
        except SessionPasswordNeeded:
            return LoginResult(success=False, needs_password=True)
        except PhoneCodeInvalid:
            return self._error("❌ Invalid OTP")
        except PhoneCodeExpired:
            return self._error("❌ OTP expired")
        except Exception as e:
            log.error(f"Pyro verify failed: {e}")
            return self._error(f"❌ {e}")
    
    async def verify_password(
        self, phone: str, password: str
    ) -> LoginResult:
        try:
            client = self._get_client(phone)
            await client.check_password(password)
            return await self._extract(client)
        except Exception as e:
            return self._error(f"❌ 2FA failed: {e}")
    
    async def _extract(self, client: Client) -> LoginResult:
        try:
            me = await client.get_me()
            data = SessionUtils.extract_from_pyrogram(client)
            session = UniversalSession(
                auth_key=data["auth_key"],
                dc_id=data["dc_id"],
                user_id=data["user_id"],
                api_id=self.api_id,
                api_hash=self.api_hash,
                is_bot=data["is_bot"],
                phone=data.get("phone"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                username=data.get("username"),
            )
            log.info(f"Pyro login success: {me.id}")
            return LoginResult(success=True, session=session)
        except Exception as e:
            return self._error(f"Extract failed: {e}")
    
    async def cleanup(self) -> None:
        for phone, client in list(self._clients.items()):
            try:
                await client.disconnect()
            except Exception:
                pass
            finally:
                self._clients.pop(phone, None)
