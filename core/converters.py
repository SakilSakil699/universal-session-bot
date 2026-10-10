"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Universal session converter.
Converts UniversalSession to/from all supported formats.

Formats:
- Pyrogram String   : >BI?256sQ? packed → base64
- Telethon String   : "1" + base64(dc_id + ip + port + auth_key)
- GramJS Hex        : same as pyro but hex-encoded
- Mtcute v3         : version byte + base64
- JSON              : plain dict
- Auth Key String   : <hex>:<dc_id>
"""
import struct
import base64
import json

from .universal_session import UniversalSession
from .exceptions import ConversionError, InvalidSessionError
from config.constants import DC_IPS, DC_PORTS


class SessionConverter:
    """
    Stateless converter. All methods are static.
    """
    
    # ═══════════════════════════════════════════════
    #  UniversalSession → Format String
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def to_pyrogram(s: UniversalSession) -> str:
        """Pyrogram format: >BI?256sQ? → base64."""
        try:
            packed = struct.pack(
                ">BI?256sQ?",
                s.dc_id, s.api_id, s.test_mode,
                s.auth_key, s.user_id, s.is_bot,
            )
            return base64.urlsafe_b64encode(packed).decode().rstrip("=")
        except struct.error as e:
            raise ConversionError(f"Pyrogram pack failed: {e}")
    
    @staticmethod
    def to_telethon(s: UniversalSession) -> str:
        """Telethon StringSession format."""
        try:
            ip = DC_IPS.get(s.dc_id, "149.154.167.51")
            ip_bytes = bytes(map(int, ip.split(".")))
            port = DC_PORTS.get(s.dc_id, 443)
            
            packed = (
                struct.pack(">B", s.dc_id)
                + ip_bytes
                + struct.pack(">H", port)
                + s.auth_key
            )
            encoded = base64.urlsafe_b64encode(packed).decode()
            return "1" + encoded
        except Exception as e:
            raise ConversionError(f"Telethon pack failed: {e}")
    
    @staticmethod
    def to_gramjs(s: UniversalSession) -> str:
        """GramJS hex format."""
        try:
            packed = struct.pack(
                ">BI?256sQ?",
                s.dc_id, s.api_id, s.test_mode,
                s.auth_key, s.user_id, s.is_bot,
            )
            return packed.hex()
        except struct.error as e:
            raise ConversionError(f"GramJS pack failed: {e}")
    
    @staticmethod
    def to_mtcute(s: UniversalSession) -> str:
        """Mtcute v3 string session."""
        try:
            version = struct.pack(">B", 3)
            packed = version + struct.pack(
                ">BI?256sQ?",
                s.dc_id, s.api_id, s.test_mode,
                s.auth_key, s.user_id, s.is_bot,
            )
            return base64.urlsafe_b64encode(packed).decode()
        except struct.error as e:
            raise ConversionError(f"Mtcute pack failed: {e}")
    
    @staticmethod
    def to_json(s: UniversalSession) -> str:
        """Simple JSON string."""
        return json.dumps(s.to_dict(), indent=2)
    
    @staticmethod
    def to_auth_key_string(s: UniversalSession) -> str:
        """Format: <hex_auth_key>:<dc_id>"""
        return f"{s.auth_key_hex}:{s.dc_id}"
    
    # ═══════════════════════════════════════════════
    #  Format String → UniversalSession
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def from_pyrogram(
        string: str, api_id: int, api_hash: str
    ) -> UniversalSession:
        try:
            padding = "=" * (-len(string) % 4)
            packed = base64.urlsafe_b64decode(string + padding)
            dc_id, api_id_, test_mode, auth_key, user_id, is_bot = (
                struct.unpack(">BI?256sQ?", packed)
            )
            return UniversalSession(
                auth_key=auth_key, dc_id=dc_id, user_id=user_id,
                api_id=api_id_ or api_id, api_hash=api_hash,
                is_bot=is_bot, test_mode=test_mode,
            )
        except Exception as e:
            raise InvalidSessionError(f"Invalid Pyrogram session: {e}")
    
    @staticmethod
    def from_telethon(
        string: str, api_id: int, api_hash: str
    ) -> UniversalSession:
        try:
            if not string.startswith("1"):
                raise ValueError("Telethon session must start with '1'")
            data = string[1:]
            padding = "=" * (-len(data) % 4)
            packed = base64.urlsafe_b64decode(data + padding)
            dc_id = packed[0]
            auth_key = packed[7:7 + 256]
            return UniversalSession(
                auth_key=auth_key, dc_id=dc_id, user_id=0,
                api_id=api_id, api_hash=api_hash,
            )
        except Exception as e:
            raise InvalidSessionError(f"Invalid Telethon session: {e}")
    
    @staticmethod
    def from_gramjs(
        hex_string: str, api_id: int, api_hash: str
    ) -> UniversalSession:
        try:
            packed = bytes.fromhex(hex_string)
            dc_id, api_id_, test_mode, auth_key, user_id, is_bot = (
                struct.unpack(">BI?256sQ?", packed)
            )
            return UniversalSession(
                auth_key=auth_key, dc_id=dc_id, user_id=user_id,
                api_id=api_id_ or api_id, api_hash=api_hash,
                is_bot=is_bot, test_mode=test_mode,
            )
        except Exception as e:
            raise InvalidSessionError(f"Invalid GramJS session: {e}")
    
    @staticmethod
    def from_auth_key_string(
        string: str, api_id: int, api_hash: str
    ) -> UniversalSession:
        try:
            hex_key, dc_id = string.split(":")
            return UniversalSession(
                auth_key=bytes.fromhex(hex_key),
                dc_id=int(dc_id), user_id=0,
                api_id=api_id, api_hash=api_hash,
            )
        except Exception as e:
            raise InvalidSessionError(f"Invalid auth_key format: {e}")
    
    # ═══════════════════════════════════════════════
    #  Batch Conversion
    # ═══════════════════════════════════════════════
    
    @classmethod
    def convert_all(cls, s: UniversalSession) -> dict:
        """Convert to all supported formats at once."""
        results = {}
        for name, fn in [
            ("pyrogram", cls.to_pyrogram),
            ("telethon", cls.to_telethon),
            ("gramjs", cls.to_gramjs),
            ("mtcute", cls.to_mtcute),
            ("json", cls.to_json),
            ("auth_key", cls.to_auth_key_string),
        ]:
            try:
                results[name] = fn(s)
            except ConversionError:
                pass
        return results
