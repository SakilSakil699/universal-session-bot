
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Telethon login engine — primary, stable.
"""
import logging
from typing import Dict

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    FloodWaitError,
    PhoneNumberInvalidError,
)

from .base import BaseEngine, LoginResult
from core.universal_session import UniversalSession
from core.session_utils import SessionUtils

log = logging.getLogger(__name__)


class TelethonEngine(BaseEngine):
    """
    Telethon-based login.
    Keeps temp clients in memory during login flow.
    """
    
    NAME = "telethon"
    DISPLAY_NAME = "⚡ Telethon"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clients: Dict[str, TelegramClient] = {}
    
    def _get_client(self, phone: str) -> TelegramClient:
        """Get or create Telethon client for this phone."""
        if phone not in self._clients:
            self._clients[phone] = TelegramClient(
                StringSession(),
                self.api_id,
                self.api_hash,
                proxy=self.proxy,
                device_model="Universal Session Bot",
                system_version="v1.0",
                app_version="v1.0",
                lang_code="en",
                system_lang_code="en-US",
            )
        return self._clients[phone]
    
    async def send_code(self, phone: str) -> LoginResult:
        try:
            client = self._get_client(phone)
            if not client.is_connected():
                await client.connect()
            
            sent = await client.send_code_request(phone)
            log.info(f"OTP sent to {phone[:5]}***")
            
            return LoginResult(
                success=True,
                phone_code_hash=sent.phone_code_hash,
                needs_code=True,
            )
        except PhoneNumberInvalidError:
            return self._error("❌ Invalid phone number format")
        except FloodWaitError as e:
            return self._error(f"⏳ Flood wait: {e.seconds}s. Try later.")
        except Exception as e:
            log.error(f"send_code failed: {e}")
            return self._error(f"❌ {e}")
    
    async def verify_code(
        self, phone: str, code: str, phone_code_hash: str
    ) -> LoginResult:
        try:
            client = self._get_client(phone)
            if not client.is_connected():
                await client.connect()
            
            await client.sign_in(
                phone=phone,
                code=code,
                phone_code_hash=phone_code_hash,
            )
            
            return await self._extract(client)
        
        except SessionPasswordNeededError:
            return LoginResult(success=False, needs_password=True)
        except PhoneCodeInvalidError:
            return self._error("❌ Invalid OTP. Try again.")
        except PhoneCodeExpiredError:
            return self._error("❌ OTP expired. Request new code.")
        except FloodWaitError as e:
            return self._error(f"⏳ Flood wait: {e.seconds}s")
        except Exception as e:
            log.error(f"verify_code failed: {e}")
            return self._error(f"❌ {e}")
    
    async def verify_password(
        self, phone: str, password: str
    ) -> LoginResult:
        try:
            client = self._get_client(phone)
            await client.sign_in(password=password)
            return await self._extract(client)
        except Exception as e:
            log.error(f"verify_password failed: {e}")
            return self._error(f"❌ 2FA failed: {e}")
    
    async def _extract(self, client: TelegramClient) -> LoginResult:
        """Extract session data from logged-in client."""
        try:
            me = await client.get_me()
            data = SessionUtils.extract_from_telethon(client)
            
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
            
            log.info(f"Login success: user_id={me.id}")
            return LoginResult(success=True, session=session)
        except Exception as e:
            log.error(f"Extract failed: {e}")
            return self._error(f"Extract failed: {e}")
    
    async def cleanup(self) -> None:
        """Disconnect all temp clients."""
        for phone, client in list(self._clients.items()):
            try:
                if client.is_connected():
                    await client.disconnect()
            except Exception:
                pass
            finally:
                self._clients.pop(phone, None)
