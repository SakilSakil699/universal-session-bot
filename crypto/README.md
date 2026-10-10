# 🔐 Crypto Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Zero-knowledge encryption for session storage.

---

## 🛡️ Security Stack

| Layer | Algorithm | Purpose |
|-------|-----------|---------|
| KDF | Argon2id (64MB, 4 iter) | Password → Key |
| Cipher | AES-256-GCM | Authenticated encryption |
| Random | `os.urandom` / `secrets` | CSPRNG |
| Compare | `hmac.compare_digest` | Timing-safe |

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `kdf.py` | Argon2id key derivation |
| `key_utils.py` | Encoding, validation, random gen |
| `vault.py` | High-level encrypt/decrypt API |
| `README.md` | This file |

---

## 💻 Usage

### Initialize vault

```python
from crypto import SessionVault
from config import settings

vault = SessionVault(settings.ENCRYPTION_KEY)
