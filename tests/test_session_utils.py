"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Unit tests for SessionUtils.
"""
import pytest
from datetime import datetime, timedelta

from core import SessionUtils, UniversalSession, InvalidSessionError


class TestValidation:
    def test_validate_valid_session(self, sample_session):
        assert SessionUtils.validate_session(sample_session) is True

    def test_validate_bad_auth_key_length(self, sample_session):
        sample_session.auth_key = b"\x00" * 100
        with pytest.raises(InvalidSessionError):
            SessionUtils.validate_auth_key(sample_session.auth_key)

    def test_validate_all_zero_auth_key(self):
        with pytest.raises(InvalidSessionError):
            SessionUtils.validate_auth_key(b"\x00" * 256)

    def test_validate_bad_dc_id(self):
        with pytest.raises(InvalidSessionError):
            SessionUtils.validate_dc_id(99)


class TestFingerprint:
    def test_fingerprint_deterministic(self, sample_auth_key):
        fp1 = SessionUtils.auth_key_fingerprint(sample_auth_key)
        fp2 = SessionUtils.auth_key_fingerprint(sample_auth_key)
        assert fp1 == fp2

    def test_fingerprint_length(self, sample_auth_key):
        fp = SessionUtils.auth_key_fingerprint(sample_auth_key)
        assert len(fp) == 16

    def test_session_hash(self, sample_session):
        h = SessionUtils.session_hash(sample_session)
        assert len(h) == 64  # SHA-256


class TestCloning:
    def test_clone(self, sample_session):
        clone = SessionUtils.clone(sample_session)
        assert clone.auth_key == sample_session.auth_key
        assert clone.user_id == sample_session.user_id
        # Different object
        assert clone is not sample_session

    def test_is_same_session(self, sample_session):
        clone = SessionUtils.clone(sample_session)
        assert SessionUtils.is_same_session(sample_session, clone)


class TestMasking:
    def test_mask_session_string(self):
        s = "A" * 200
        masked = SessionUtils.mask_session_string(s, show=20)
        assert "..." in masked
        assert masked.startswith("A" * 20)
        assert masked.endswith("A" * 20)

    def test_mask_short(self):
        masked = SessionUtils.mask_session_string("short", show=20)
        assert masked == "short***"


class TestAge:
    def test_age_string_just_now(self):
        now = datetime.utcnow()
        result = SessionUtils.age_string(now)
        assert "s ago" in result

    def test_age_string_hours(self):
        past = datetime.utcnow() - timedelta(hours=3)
        result = SessionUtils.age_string(past)
        assert "3h ago" in result

    def test_age_string_days(self):
        past = datetime.utcnow() - timedelta(days=2)
        result = SessionUtils.age_string(past)
        assert "2d ago" in result
