# 🗄️ DB Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Async database layer — SQLAlchemy 2.0 + PostgreSQL/SQLite.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `database.py` | Async engine + session factory |
| `models.py` | User, Session, ActivityLog tables |
| `crud.py` | Create/Read/Update/Delete helpers |
| `README.md` | This file |

---

## 🗄️ Schema

### `users`
| Column | Type | Notes |
|--------|------|-------|
| `id` | BigInteger PK | Telegram user ID |
| `username` | String(64) | |
| `first_name` | String(128) | |
| `last_name` | String(128) | |
| `language_code` | String(8) | |
| `is_premium` | Boolean | |
| `is_banned` | Boolean | |
| `is_admin` | Boolean | |
| `session_count` | Integer | Denormalized counter |
| `last_active` | DateTime | |
| `created_at` | DateTime | |

### `sessions`
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | Auto |
| `user_id` | FK → users.id | CASCADE |
| `label` | String(64) | Optional nickname |
| `engine` | String(16) | telethon/pyrogram/ferogram |
| `dc_id` | Integer | 1-5 |
| `tg_user_id` | BigInteger | Telegram user ID in session |
| `phone` | String(32) | |
| `first_name` | String(128) | |
| `username` | String(64) | |
| `is_bot` | Boolean | |
| **`encrypted_data`** | **Text** | **AES-256-GCM blob (base64)** |
| `fingerprint` | String(16) | SHA-256 short, indexed |
| `is_active` | Boolean | |
| `created_at` | DateTime | |

### `activity_logs`
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | Auto |
| `user_id` | FK → users.id | CASCADE |
| `action` | String(32) | e.g. `session_create` |
| `detail` | Text | Optional JSON |
| `ip` | String(64) | |
| `success` | Boolean | |
| `created_at` | DateTime | Indexed |

---

## 💻 Usage

### Initialize

```python
from db import db

await db.init()      # Create engine + tables
# ... run bot ...
await db.close()     # On shutdown
