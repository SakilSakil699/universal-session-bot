
# 📦 Session Formats Reference

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Every Telegram session format supported by this bot — with full specs.

---

## 🎯 Overview

| # | Format | Library | Type | Size | Use Case |
|---|--------|---------|------|------|----------|
| 1 | **Pyrogram String** | Pyrogram | String | ~360 chars | Python automation |
| 2 | **Telethon String** | Telethon | String | ~360 chars | Python scripts |
| 3 | **GramJS Hex** | GramJS | String | ~540 chars | Node.js apps |
| 4 | **Mtcute v3** | Mtcute | String | ~365 chars | Modern TS/JS |
| 5 | **JSON** | Custom | JSON | ~500 chars | Debugging |
| 6 | **Auth Key** | MTProto | String | ~520 chars | Low-level |
| 7 | **TData** | TG Desktop | Folder | ~10 KB | Desktop app |
| 8 | **Android tgnet** | Android | File | ~1 KB | Android app |
| 9 | **Ferogram** | Ferogram | String | ~360 chars | Rust core |

---

## 📐 Format Specifications

### 1. Pyrogram String

**Binary struct:** `>BI?256sQ?`
