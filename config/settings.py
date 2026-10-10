"""
Advanced configuration loader with validation.
Loads from environment variables with type safety.
"""
import os
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv

# Load .env from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings:
    """
    Central settings class.
    All config values validated at startup.
    """
    
    # ── Telegram API ─────────────────────────────
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # ── Owner & Admin ────────────────────────────
    OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))
    ADMIN_IDS: List[int] = [
        int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
    ]
    
    # ── Database ─────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/sessionbot"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # ── Security ─────────────────────────────────
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")
    
    # ── Rate Limiting ────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "5"))
    MAX_SESSIONS_PER_USER: int = int(os.getenv("MAX_SESSIONS_PER_USER", "10"))
    
    # ── Features ─────────────────────────────────
    ENABLE_FEROGRAM: bool = os.getenv("ENABLE_FEROGRAM", "false").lower() == "true"
    ENABLE_GRAMJS: bool = os.getenv("ENABLE_GRAMJS", "false").lower() == "true"
    ENABLE_TDATA: bool = os.getenv("ENABLE_TDATA", "false").lower() == "true"
    
    # ── Paths ────────────────────────────────────
    ROOT_DIR: Path = ROOT_DIR
    LOGS_DIR: Path = ROOT_DIR / "logs"
    DATA_DIR: Path = ROOT_DIR / "data"
    SESSIONS_DIR: Path = ROOT_DIR / "data" / "sessions"
    TDATA_DIR: Path = ROOT_DIR / "data" / "tdata"
    TGNET_DIR: Path = ROOT_DIR / "data" / "tgnet"
    
    # ── Logging ──────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """Validate critical settings. Raises if anything missing."""
        errors = []
        
        if not cls.API_ID:
            errors.append("API_ID is missing")
        if not cls.API_HASH:
            errors.append("API_HASH is missing")
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is missing")
        if not cls.OWNER_ID:
            errors.append("OWNER_ID is missing")
        if len(cls.ENCRYPTION_KEY) < 32:
            errors.append("ENCRYPTION_KEY must be at least 32 chars")
        
        if errors:
            raise ValueError(
                "❌ Config validation failed:\n  • " + "\n  • ".join(errors)
            )
        
        # Create directories
        for d in [cls.LOGS_DIR, cls.SESSIONS_DIR, cls.TDATA_DIR, cls.TGNET_DIR]:
            d.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if user is admin or owner."""
        return user_id == cls.OWNER_ID or user_id in cls.ADMIN_IDS


settings = Settings()
