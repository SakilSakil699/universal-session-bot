# 🎮 Handlers Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

All bot command & callback handlers.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `start.py` | `/start`, `/help`, `/about`, menu callbacks |
| `session_gen.py` | `/newsession` — login flow |
| `convert.py` | Format selection & output |
| `my_sessions.py` | `/mysessions` — user's sessions |
| `admin.py` | Owner panel — stats, broadcast |

---

## 🎯 Command Reference

| Command | Access | Description |
|---------|--------|-------------|
| `/start` | All | Welcome menu |
| `/help` | All | Help & commands |
| `/about` | All | Bot info + credits |
| `/newsession` | All | Create session |
| `/mysessions` | All | View saved sessions |
| `/cancel` | All | Cancel current flow |
| `/admin` | Owner | Admin panel |

---

## 🔄 Session Flow (FSM)
