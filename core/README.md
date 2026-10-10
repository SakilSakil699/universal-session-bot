# 🧠 Core Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Session conversion, parsing & utilities — the brain of the bot.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `universal_session.py` | `UniversalSession` dataclass |
| `converters.py` | Format ↔ Format conversion |
| `session_parser.py` | Auto-detect & parse any format |
| `session_utils.py` | Validation, fingerprint, extract helpers |
| `exceptions.py` | Custom exception hierarchy |

---

## 🎯 Supported Formats

| Format | Direction | Notes |
|--------|-----------|-------|
| **Pyrogram String** | ↔ | `>BI?256sQ?` → base64 |
| **Telethon String** | ↔ | `"1" + base64` |
| **GramJS Hex** | ↔ | Same as pyro, hex-encoded |
| **Mtcute v3** | → | Version byte + base64 |
| **JSON** | ↔ | Plain dict |
| **Auth Key** | ↔ | `<hex>:<dc_id>` |

---

## 🏗️ Architecture
