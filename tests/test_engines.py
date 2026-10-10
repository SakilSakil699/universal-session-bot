
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Unit tests for engines module.
Tests BaseEngine, LoginResult, Telethon/Pyrogram engines, and factory.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from engines import (
    BaseEngine,
    LoginResult,
    TelethonEngine,
    PyrogramEngine,
    get_engine,
    available_engines,
    __version__,
    __author_username__,
)
from core import UniversalSession


# ═══════════════════════════════════════════════
#  LoginResult Tests
# ═══════════════════════════════════════════════

class TestLoginResult:
    def test_default_values(self):
        r = LoginResult(success=True)
        assert r.success is True
        assert r.session is None
        assert r.phone_code_hash is None
        assert r.needs_password is False
        assert r.needs_code is False
        assert r.error is None

    def test_needs_code_result(self):
        r = LoginResult(success=True, phone_code_hash="abc", needs_code=True)
        assert r.needs_code is True
        assert r.phone_code_hash == "abc"

    def test_error_result(self):
        r = LoginResult(success=False, error="Invalid phone")
        assert r.success is False
        assert r.error == "Invalid phone"

    def test_with_session(self, sample_session):
        r = LoginResult(success=True, session=sample_session)
        assert r.session is sample_session


# ═══════════════════════════════════════════════
#  BaseEngine Tests
# ═══════════════════════════════════════════════

class TestBaseEngine:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseEngine(api_id=1, api_hash="x")

    def test_abstract_methods_defined(self):
        assert BaseEngine.__abstractmethods__ == frozenset({
            "send_code", "verify_code", "verify_password", "cleanup",
        })

    def test_error_helper(self):
        """Subclass must implement abstract methods to test _error."""
        class DummyEngine(BaseEngine):
            NAME = "dummy"
            DISPLAY_NAME = "Dummy"
            async def send_code(self, phone): ...
            async def verify_code(self, phone, code, h): ...
            async def verify_password(self, phone, pw): ...
            async def cleanup(self): ...

        e = DummyEngine(api_id=1, api_hash="x")
        r = e._error("test error")
        assert r.success is False
        assert r.error == "test error"

    def test_engine_stores_credentials(self):
        class DummyEngine(BaseEngine):
            NAME = "dummy"
            async def send_code(self, phone): ...
            async def verify_code(self, phone, code, h): ...
            async def verify_password(self, phone, pw): ...
            async def cleanup(self): ...

        e = DummyEngine(api_id=12345, api_hash="abcdef", proxy={"http": "x"})
        assert e.api_id == 12345
        assert e.api_hash == "abcdef"
        assert e.proxy == {"http": "x"}


# ═══════════════════════════════════════════════
#  Engine Metadata Tests
# ═══════════════════════════════════════════════

class TestEngineMetadata:
    def test_telethon_name(self):
        assert TelethonEngine.NAME == "telethon"
        assert "Telethon" in TelethonEngine.DISPLAY_NAME

    def test_pyrogram_name(self):
        assert PyrogramEngine.NAME == "pyrogram"
        assert "Pyrogram" in PyrogramEngine.DISPLAY_NAME

    def test_telethon_subclass_of_base(self):
        assert issubclass(TelethonEngine, BaseEngine)

    def test_pyrogram_subclass_of_base(self):
        assert issubclass(PyrogramEngine, BaseEngine)


# ═══════════════════════════════════════════════
#  TelethonEngine Tests (mocked)
# ═══════════════════════════════════════════════

class TestTelethonEngine:
    def test_init(self):
        e = TelethonEngine(api_id=12345, api_hash="abc")
        assert e.api_id == 12345
        assert e.api_hash == "abc"
        assert e._clients == {}

    @pytest.mark.asyncio
    async def test_send_code_success(self):
        e = TelethonEngine(api_id=12345, api_hash="abc")

        mock_sent = MagicMock()
        mock_sent.phone_code_hash = "abc123"

        mock_client = AsyncMock()
        mock_client.is_connected = MagicMock(return_value=True)
        mock_client.send_code_request = AsyncMock(return_value=mock_sent)

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.send_code("+919876543210")

        assert result.success is True
        assert result.phone_code_hash == "abc123"
        assert result.needs_code is True

    @pytest.mark.asyncio
    async def test_send_code_invalid_phone(self):
        from telethon.errors import PhoneNumberInvalidError

        e = TelethonEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.is_connected = MagicMock(return_value=True)
        mock_client.send_code_request = AsyncMock(
            side_effect=PhoneNumberInvalidError(request=None)
        )

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.send_code("+911")

        assert result.success is False
        assert "Invalid phone" in result.error

    @pytest.mark.asyncio
    async def test_verify_code_needs_password(self):
        from telethon.errors import SessionPasswordNeededError

        e = TelethonEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.is_connected = MagicMock(return_value=True)
        mock_client.sign_in = AsyncMock(
            side_effect=SessionPasswordNeededError(request=None)
        )

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.verify_code("+919876543210", "12345", "hash")

        assert result.success is False
        assert result.needs_password is True

    @pytest.mark.asyncio
    async def test_verify_code_invalid_otp(self):
        from telethon.errors import PhoneCodeInvalidError

        e = TelethonEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.is_connected = MagicMock(return_value=True)
        mock_client.sign_in = AsyncMock(
            side_effect=PhoneCodeInvalidError(request=None)
        )

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.verify_code("+919876543210", "99999", "hash")

        assert result.success is False
        assert "Invalid OTP" in result.error

    @pytest.mark.asyncio
    async def test_cleanup_disconnects_clients(self):
        e = TelethonEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.is_connected = MagicMock(return_value=True)
        mock_client.disconnect = AsyncMock()

        e._clients["+911111111111"] = mock_client
        e._clients["+912222222222"] = mock_client

        await e.cleanup()

        assert mock_client.disconnect.call_count == 2
        assert e._clients == {}


# ═══════════════════════════════════════════════
#  PyrogramEngine Tests (mocked)
# ═══════════════════════════════════════════════

class TestPyrogramEngine:
    def test_init(self):
        e = PyrogramEngine(api_id=12345, api_hash="abc")
        assert e.api_id == 12345
        assert e._clients == {}

    @pytest.mark.asyncio
    async def test_send_code_success(self):
        e = PyrogramEngine(api_id=12345, api_hash="abc")

        mock_sent = MagicMock()
        mock_sent.phone_code_hash = "pyro_hash"

        mock_client = AsyncMock()
        mock_client.connect = AsyncMock()
        mock_client.send_code = AsyncMock(return_value=mock_sent)

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.send_code("+919876543210")

        assert result.success is True
        assert result.phone_code_hash == "pyro_hash"
        assert result.needs_code is True

    @pytest.mark.asyncio
    async def test_send_code_invalid_phone(self):
        from pyrogram.errors import PhoneNumberInvalid

        e = PyrogramEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.connect = AsyncMock()
        mock_client.send_code = AsyncMock(
            side_effect=PhoneNumberInvalid()
        )

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.send_code("+911")

        assert result.success is False
        assert "Invalid phone" in result.error

    @pytest.mark.asyncio
    async def test_verify_code_needs_password(self):
        from pyrogram.errors import SessionPasswordNeeded

        e = PyrogramEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.sign_in = AsyncMock(
            side_effect=SessionPasswordNeeded()
        )

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.verify_code("+919876543210", "12345", "hash")

        assert result.success is False
        assert result.needs_password is True

    @pytest.mark.asyncio
    async def test_verify_code_invalid_otp(self):
        from pyrogram.errors import PhoneCodeInvalid

        e = PyrogramEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.sign_in = AsyncMock(side_effect=PhoneCodeInvalid())

        with patch.object(e, "_get_client", return_value=mock_client):
            result = await e.verify_code("+919876543210", "99999", "hash")

        assert result.success is False
        assert "Invalid OTP" in result.error

    @pytest.mark.asyncio
    async def test_cleanup(self):
        e = PyrogramEngine(api_id=12345, api_hash="abc")

        mock_client = AsyncMock()
        mock_client.disconnect = AsyncMock()

        e._clients["+911111111111"] = mock_client

        await e.cleanup()

        mock_client.disconnect.assert_awaited_once()
        assert e._clients == {}


# ═══════════════════════════════════════════════
#  Factory Tests
# ═══════════════════════════════════════════════

class TestEngineFactory:
    def test_get_engine_telethon(self):
        e = get_engine("telethon", api_id=123, api_hash="abc")
        assert isinstance(e, TelethonEngine)

    def test_get_engine_pyrogram(self):
        e = get_engine("pyrogram", api_id=123, api_hash="abc")
        assert isinstance(e, PyrogramEngine)

    def test_get_engine_case_insensitive(self):
        e = get_engine("TELETHON", api_id=123, api_hash="abc")
        assert isinstance(e, TelethonEngine)

    def test_get_engine_invalid(self):
        with pytest.raises(ValueError, match="Unknown engine"):
            get_engine("nonexistent", api_id=123, api_hash="abc")

    def test_get_engine_with_proxy(self):
        e = get_engine(
            "telethon", api_id=123, api_hash="abc",
            proxy={"http": "http://127.0.0.1:8080"},
        )
        assert e.proxy == {"http": "http://127.0.0.1:8080"}

    def test_available_engines(self):
        engines = available_engines()
        assert "telethon" in engines
        assert "pyrogram" in engines
        assert isinstance(engines, list)


# ═══════════════════════════════════════════════
#  Module Metadata Tests
# ═══════════════════════════════════════════════

class TestModuleMetadata:
    def test_version(self):
        assert __version__ == "1.0.0"

    def test_author(self):
        assert __author_username__ == "@YO_UR_OFFICIAL_CRUSH"
