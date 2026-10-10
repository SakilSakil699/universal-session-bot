"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Unit tests for UniversalSession dataclass.
"""
import pytest

from core import UniversalSession


class TestProperties:
    def test_full_name(self, sample_session):
        assert sample_session.full_name == "Sakil Khan"

    def test_full_name_fallback(self, sample_auth_key):
        s = UniversalSession(
            auth_key=sample_auth_key, dc_id=4, user_id=1,
            api_id=1, api_hash="x",
        )
        assert s.full_name == "Unknown"

    def test_auth_key_hex(self, sample_session):
        assert len(sample_session.auth_key_hex) == 512

    def test_dc_location(self, sample_session):
        assert "Amsterdam" in sample_session.dc_location


class TestSerialization:
    def test_to_dict(self, sample_session):
        d = sample_session.to_dict()
        assert "auth_key_hex" in d
        assert d["dc_id"] == 4
        assert d["user_id"] == 123456789

    def test_to_dict_hidden_secrets(self, sample_session):
        d = sample_session.to_dict(hide_secrets=True)
        assert "auth_key_hex" not in d
        assert d["phone"] == "***"

    def test_from_dict_roundtrip(self, sample_session):
        d = sample_session.to_dict()
        restored = UniversalSession.from_dict(d)
        assert restored.auth_key == sample_session.auth_key
        assert restored.user_id == sample_session.user_id
        assert restored.dc_id == sample_session.dc_id


class TestRepr:
    def test_repr_no_secrets(self, sample_session):
        r = repr(sample_session)
        assert sample_session.auth_key_hex not in r
        assert "user_id=123456789" in r
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
