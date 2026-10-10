
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Unit tests for SessionConverter.
"""
import base64
import pytest

from core import (
    UniversalSession,
    SessionConverter,
    ConversionError,
    InvalidSessionError,
)


class TestPyrogramConversion:
    def test_to_pyrogram(self, sample_session):
        s = SessionConverter.to_pyrogram(sample_session)
        assert isinstance(s, str)
        assert len(s) > 200

    def test_pyrogram_roundtrip(self, sample_session):
        encoded = SessionConverter.to_pyrogram(sample_session)
        decoded = SessionConverter.from_pyrogram(
            encoded, sample_session.api_id, sample_session.api_hash
        )
        assert decoded.auth_key == sample_session.auth_key
        assert decoded.dc_id == sample_session.dc_id
        assert decoded.user_id == sample_session.user_id
        assert decoded.is_bot == sample_session.is_bot

    def test_pyrogram_invalid(self):
        with pytest.raises(InvalidSessionError):
            SessionConverter.from_pyrogram("not_a_session", 1, "x")


class TestTelethonConversion:
    def test_to_telethon(self, sample_session):
        s = SessionConverter.to_telethon(sample_session)
        assert s.startswith("1")
        assert len(s) > 200

    def test_telethon_roundtrip(self, sample_session):
        encoded = SessionConverter.to_telethon(sample_session)
        decoded = SessionConverter.from_telethon(
            encoded, sample_session.api_id, sample_session.api_hash
        )
        assert decoded.auth_key == sample_session.auth_key
        assert decoded.dc_id == sample_session.dc_id

    def test_telethon_must_start_with_1(self):
        with pytest.raises(InvalidSessionError):
            SessionConverter.from_telethon("Xnotvalid", 1, "x")


class TestGramJSConversion:
    def test_to_gramjs(self, sample_session):
        s = SessionConverter.to_gramjs(sample_session)
        assert isinstance(s, str)
        assert all(c in "0123456789abcdef" for c in s)
        assert len(s) == 542  # 271 bytes * 2

    def test_gramjs_roundtrip(self, sample_session):
        encoded = SessionConverter.to_gramjs(sample_session)
        decoded = SessionConverter.from_gramjs(
            encoded, sample_session.api_id, sample_session.api_hash
        )
        assert decoded.auth_key == sample_session.auth_key
        assert decoded.dc_id == sample_session.dc_id
        assert decoded.user_id == sample_session.user_id


class TestMtcuteConversion:
    def test_to_mtcute(self, sample_session):
        s = SessionConverter.to_mtcute(sample_session)
        assert isinstance(s, str)
        assert len(s) > 200

    def test_mtcute_has_version_byte(self, sample_session):
        encoded = SessionConverter.to_mtcute(sample_session)
        padding = "=" * (-len(encoded) % 4)
        raw = base64.urlsafe_b64decode(encoded + padding)
        assert raw[0] == 3  # v3


class TestJSONConversion:
    def test_to_json(self, sample_session):
        s = SessionConverter.to_json(sample_session)
        assert "auth_key_hex" in s
        assert "dc_id" in s
        assert "user_id" in s


class TestAuthKeyString:
    def test_to_auth_key(self, sample_session):
        s = SessionConverter.to_auth_key_string(sample_session)
        assert ":" in s
        hex_part, dc_part = s.split(":")
        assert len(hex_part) == 512
        assert dc_part == "4"

    def test_auth_key_roundtrip(self, sample_session):
        encoded = SessionConverter.to_auth_key_string(sample_session)
        decoded = SessionConverter.from_auth_key_string(
            encoded, sample_session.api_id, sample_session.api_hash
        )
        assert decoded.auth_key == sample_session.auth_key
        assert decoded.dc_id == sample_session.dc_id


class TestBatchConversion:
    def test_convert_all(self, sample_session):
        results = SessionConverter.convert_all(sample_session)
        assert "pyrogram" in results
        assert "telethon" in results
        assert "gramjs" in results
        assert "mtcute" in results
        assert "json" in results
        assert "auth_key" in results
        assert all(isinstance(v, str) for v in results.values())
