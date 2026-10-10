"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Shared pytest fixtures.
"""
import os
import sys
from pathlib import Path

import pytest

# Ensure project root on path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Set test env vars BEFORE importing config
os.environ.setdefault("API_ID", "12345")
os.environ.setdefault("API_HASH", "abcdef1234567890abcdef1234567890")
os.environ.setdefault("BOT_TOKEN", "123456:TEST-TOKEN-FOR-TESTS")
os.environ.setdefault("OWNER_ID", "999999")
os.environ.setdefault(
    "ENCRYPTION_KEY",
    "a" * 64,   # 64 hex chars
)
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./data/test.db",
)


@pytest.fixture(scope="session")
def sample_auth_key() -> bytes:
    """Deterministic 256-byte auth key for tests."""
    return b"\x42" * 256


@pytest.fixture
def sample_session(sample_auth_key):
    """A UniversalSession for testing."""
    from core import UniversalSession
    return UniversalSession(
        auth_key=sample_auth_key,
        dc_id=4,
        user_id=123456789,
        api_id=12345,
        api_hash="abc",
        first_name="Sakil",
        last_name="Khan",
        username="sakil",
    )


@pytest.fixture
def master_key() -> str:
    """Test master key (64 hex chars)."""
    return "a" * 64


@pytest.fixture
def vault(master_key):
    """SessionVault instance for tests."""
    from crypto import SessionVault
    return SessionVault(master_key)
