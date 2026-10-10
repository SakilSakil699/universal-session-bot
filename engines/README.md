# ⚡ Engines Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Multi-library Telegram login engines with a unified interface.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports + `get_engine()` factory |
| `base.py` | Abstract `BaseEngine` + `LoginResult` |
| `telethon_engine.py` | Telethon login (stable, recommended) |
| `pyro_engine.py` | Pyrogram login (fast, clean) |
| `ferogram_engine.py` | Ferogram login (Rust core, experimental) |
| `gramjs_engine.js` | GramJS worker (Node.js subprocess) |
| `gramjs_package.json` | Node.js dependencies |
| `README.md` | This file |

---

## 🎯 Available Engines

| Engine | Status | Speed | 2FA | Notes |
|--------|--------|-------|-----|-------|
| **Telethon** | ✅ Stable | Fast | ✅ | Recommended, best ecosystem |
| **Pyrogram** | ✅ Stable | Faster | ✅ | Clean API, in-memory |
| **Ferogram** | ⚠️ Experimental | Fastest | ✅ | Rust core, pre-release |
| **GramJS** | ✅ Stable | Medium | ❌ | Node.js subprocess |

---

## 🔄 Unified Login Flow

All Python engines (Telethon, Pyrogram, Ferogram) follow the **same 3-step flow**:
