"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Auto-detect session format from string.
"""
import base64
import json

from .universal_session import UniversalSession
from .converters import SessionConverter
from .exceptions import InvalidSessionError


class SessionParser:
    """Auto-detect session format and parse it."""
    
    @staticmethod
    def detect_format(string: str) -> str:
        """Returns: pyrogram, telethon, gramjs, mtcute, json, auth_key."""
        s = string.strip()
        
        if s.startswith("{"):
            return "json"
        
        if ":" in s and len(s.split(":")[0]) == 512:
            return "auth_key"
        
        if s.startswith("1") and len(s) > 100:
            try:
                padding = "=" * (-len(s[1:]) % 4)
                base64.urlsafe_b64decode(s[1:] + padding)
                return "telethon"
            except Exception:
                pass
        
        if len(s) >= 500 and all(c in "0123456789abcdefABCDEF" for c in s):
            return "gramjs"
        
        try:
            padding = "=" * (-len(s) % 4)
            packed = base64.urlsafe_b64decode(s + padding)
            if len(packed) > 270 and packed[0] == 3:
                return "mtcute"
            if len(packed) == 271:
                return "pyrogram"
        except Exception:
            pass
        
        raise InvalidSessionError(
            f"Cannot detect format. Length: {len(s)}"
        )
    
    @classmethod
    def parse(
        cls, string: str, api_id: int, api_hash: str, fmt: str = None
    ) -> UniversalSession:
        """Parse any session string into UniversalSession."""
        if fmt is None:
            fmt = cls.detect_format(string)
        
        if fmt == "json":
            data = json.loads(string)
            return UniversalSession.from_dict(data)
        
        if fmt == "mtcute":
            padding = "=" * (-len(string) % 4)
            packed = base64.urlsafe_b64decode(string + padding)
            pyro_like = base64.urlsafe_b64encode(packed[1:]).decode()
            return SessionConverter.from_pyrogram(pyro_like, api_id, api_hash)
        
        parser_map = {
            "pyrogram": SessionConverter.from_pyrogram,
            "telethon": SessionConverter.from_telethon,
            "gramjs": SessionConverter.from_gramjs,
            "auth_key": SessionConverter.from_auth_key_string,
        }
        parser = parser_map.get(fmt)
        if not parser:
            raise InvalidSessionError(f"Unsupported format: {fmt}")
        return parser(string, api_id, api_hash)
