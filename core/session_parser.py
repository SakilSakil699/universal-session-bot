
"""
Auto-detect session format from string.
User koi bhi string bheje, hum identify karke parse kar lenge.
"""
from .universal_session import UniversalSession
from .converters import SessionConverter
from .exceptions import InvalidSessionError


class SessionParser:
    """
    Auto-detect session format and parse it.
    """
    
    @staticmethod
    def detect_format(string: str) -> str:
        """
        Returns format name: 'pyrogram', 'telethon', 'gramjs',
        'mtcute', 'auth_key', or 'json'.
        """
        s = string.strip()
        
        # JSON
        if s.startswith("{"):
            return "json"
        
        # Auth key format: hex:dcid
        if ":" in s and len(s.split(":")[0]) == 512:
            return "auth_key"
        
        # Telethon: starts with "1"
        if s.startswith("1") and len(s) > 100:
            # Check if it decodes properly
            try:
                import base64
                padding = "=" * (-len(s[1:]) % 4)
                base64.urlsafe_b64decode(s[1:] + padding)
                return "telethon"
            except Exception:
                pass
        
        # GramJS: all hex, length ~530
        if len(s) >= 500 and all(c in "0123456789abcdefABCDEF" for c in s):
            return "gramjs"
        
        # Pyrogram / Mtcute: base64
        try:
            import base64
            padding = "=" * (-len(s) % 4)
            packed = base64.urlsafe_b64decode(s + padding)
            
            # Mtcute v3 has 0x03 prefix
            if len(packed) > 270 and packed[0] == 3:
                return "mtcute"
            
            # Pyrogram struct: >BI?256sQ?
            if len(packed) == 271:
                return "pyrogram"
        except Exception:
            pass
        
        raise InvalidSessionError(
            f"Cannot detect session format. Length: {len(s)}, "
            f"starts with: {s[:20]}..."
        )
    
    @classmethod
    def parse(
        cls, string: str, api_id: int, api_hash: str,
        fmt: str = None
    ) -> UniversalSession:
        """
        Parse any session string into UniversalSession.
        Auto-detects format if not provided.
        """
        if fmt is None:
            fmt = cls.detect_format(string)
        
        parser_map = {
            "pyrogram": SessionConverter.from_pyrogram,
            "telethon": SessionConverter.from_telethon,
            "gramjs": SessionConverter.from_gramjs,
            "auth_key": SessionConverter.from_auth_key_string,
        }
        
        if fmt == "json":
            import json
            data = json.loads(string)
            return UniversalSession.from_dict(data)
        
        if fmt == "mtcute":
            # Mtcute: strip version byte, treat as pyro
            import base64
            padding = "=" * (-len(string) % 4)
            packed = base64.urlsafe_b64decode(string + padding)
            # Remove first byte (version)
            pyro_like = base64.urlsafe_b64encode(packed[1:]).decode()
            return SessionConverter.from_pyrogram(pyro_like, api_id, api_hash)
        
        parser = parser_map.get(fmt)
        if not parser:
            raise InvalidSessionError(f"Unsupported format: {fmt}")
        
        return parser(string, api_id, api_hash)
