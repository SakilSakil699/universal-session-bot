
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Unit tests for crypto module.
"""
import pytest

from crypto import SessionVault, KeyDerivation, KeyUtils
from core import EncryptionError, UniversalSession


class TestKeyUtils:
    def test_generate_master_key(self):
        key = KeyUtils.generate_master_key()
        assert len(key) == 64
        assert all(c in "0123456789abcdef" for c in key)

    def test_validate_master_key_ok(self):
        key = "a" * 64
        assert KeyUtils.validate_master_key(key) is True

    def test_validate_master_key_wrong_length(self):
        with pytest.raises(EncryptionError):
            KeyUtils.validate_master_key("short")

    def test_validate_master_key_not_hex(self):
        with pytest.raises(EncryptionError):
            KeyUtils.validate_master_key("z" * 64)

    def test_b64_roundtrip(self):
        data = b"hello world"
        encoded = KeyUtils.b64_encode(data)
        decoded = KeyUtils.b64_decode(encoded)
        assert decoded == data

    def test_constant_time_compare(self):
        assert KeyUtils.constant_time_compare(b"abc", b"abc")
        assert not KeyUtils.constant_time_compare(b"abc", b"abd")


class TestKeyDerivation:
    def test_generate_salt(self):
        salt = KeyDerivation.generate_salt()
        assert len(salt) == 16

    def test_derive_key(self):
        salt = KeyDerivation.generate_salt()
        key = KeyDerivation.derive_key("password123", salt)
        assert len(key) == 32

    def test_deterministic(self):
        salt = b"\x00" * 16
        k1 = KeyDerivation.derive_key("password123", salt)
        k2 = KeyDerivation.derive_key("password123", salt)
        assert k1 == k2

    def test_different_passwords(self):
        salt = b"\x00" * 16
        k1 = KeyDerivation.derive_key("password123", salt)
        k2 = KeyDerivation.derive_key("password456", salt)
        assert k1 != k2

    def test_short_password_rejected(self):
        with pytest.raises(EncryptionError):
            KeyDerivation.derive_key("short", b"\x00" * 16)


class TestSessionVault:
    def test_encrypt_decrypt_session(self, vault, sample_session):
        encrypted = vault.encrypt_session(sample_session)
        assert isinstance(encrypted, str)
        assert len(encrypted) > 100

        decrypted = vault.decrypt_session(encrypted)
        assert decrypted.auth_key == sample_session.auth_key
        assert decrypted.dc_id == sample_session.dc_id
        assert decrypted.user_id == sample_session.user_id

    def test_encrypt_decrypt_text(self, vault):
        encrypted = vault.encrypt_text("hello world")
        decrypted = vault.decrypt_text(encrypted)
        assert decrypted == "hello world"

    def test_tampered_data_fails(self, vault, sample_session):
        encrypted = vault.encrypt_session(sample_session)
        # Corrupt
        tampered = encrypted[:-10] + "XXXXXXXXXX"
        with pytest.raises(EncryptionError):
            vault.decrypt_session(tampered)

    def test_wrong_key_fails(self, sample_session):
        v1 = SessionVault("a" * 64)
        v2 = SessionVault("b" * 64)
        encrypted = v1.encrypt_session(sample_session)
        with pytest.raises(EncryptionError):
            v2.decrypt_session(encrypted)
