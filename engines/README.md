# ⚡ Engines Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Multi-library Telegram login engines.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `base.py` | Abstract `BaseEngine` + `LoginResult` |
| `telethon_engine.py` | Telethon login (stable) |
| `pyro_engine.py` | Pyrogram login (fast) |
| `ferogram_engine.py` | Ferogram login (optional, Rust core) |
| `README.md` | This file |

---

## 🎯 Available Engines

| Engine | Status | Speed | Notes |
|--------|--------|-------|-------|
| **Telethon** | ✅ Stable | Fast | Recommended, best ecosystem |
| **Pyrogram** | ✅ Stable | Faster | Clean API, in-memory sessions |
| **Ferogram** | ⚠️ Experimental | Fastest | Rust core, pre-release |

---

## 🔄 Login Flow

All engines follow the **same 3-step flow**:
