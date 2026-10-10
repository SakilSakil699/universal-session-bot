"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Unit tests for validators.
"""
import pytest

from utils import Validators


class TestPhoneValidation:
    @pytest.mark.parametrize("phone", [
        "+919876543210",
        "+14155551234",
        "+447911123456",
        "+919876543210",
    ])
    def test_valid_phones(self, phone):
        assert Validators.is_valid_phone(phone)

    @pytest.mark.parametrize("phone", [
        "919876543210",       # no +
        "+91",                # too short
        "+91987654321012345", # too long
        "not_a_phone",
        "",
        None,
    ])
    def test_invalid_phones(self, phone):
        assert not Validators.is_valid_phone(phone)

    def test_normalize(self):
        assert Validators.normalize_phone("+91 9876-543 210") == "+919876543210"


class TestOTPValidation:
    @pytest.mark.parametrize("otp", ["12345", "1 2 3 4 5", "1234", "123456"])
    def test_valid_otps(self, otp):
        assert Validators.is_valid_otp(otp)

    @pytest.mark.parametrize("otp", ["", "abcde", "123", "12345678"])
    def test_invalid_otps(self, otp):
        assert not Validators.is_valid_otp(otp)


class TestSessionValidation:
    def test_valid_session_string(self):
        s = "A" * 200
        assert Validators.is_valid_session_string(s)

    def test_invalid_short(self):
        assert not Validators.is_valid_session_string("short")

    def test_invalid_whitespace(self):
        s = "A" * 100 + " " + "B" * 100
        assert not Validators.is_valid_session_string(s)


class TestAuthKeyValidation:
    def test_valid_auth_key_hex(self):
        assert Validators.is_valid_auth_key_hex("ab" * 256)

    def test_invalid_length(self):
        assert not Validators.is_valid_auth_key_hex("ab" * 100)

    def test_invalid_hex(self):
        assert not Validators.is_valid_auth_key_hex("zz" * 256)


class TestDCValidation:
    @pytest.mark.parametrize("dc", [1, 2, 3, 4, 5, "4"])
    def test_valid_dcs(self, dc):
        assert Validators.is_valid_dc_id(dc)

    @pytest.mark.parametrize("dc", [0, 6, -1, "abc"])
    def test_invalid_dcs(self, dc):
        assert not Validators.is_valid_dc_id(dc)


class TestFileValidation:
    @pytest.mark.parametrize("fname", ["s.session", "data.json", "notes.txt", "x.zip"])
    def test_allowed_files(self, fname):
        assert Validators.is_allowed_file(fname)

    @pytest.mark.parametrize("fname", ["virus.exe", "script.sh", "image.png", ""])
    def test_disallowed_files(self, fname):
        assert not Validators.is_allowed_file(fname)


class TestMasking:
    def test_mask_phone(self):
        masked = Validators.mask_phone("+919876543210")
        assert "****" in masked
        assert masked.startswith("+91")
        assert masked.endswith("3210")
