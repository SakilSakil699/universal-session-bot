# 🤖 Bot Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Main entry point & dispatcher setup.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `main.py` | Bot initialization, router registration, polling |
| `README.md` | This file |

---

## 🚀 Run the Bot

### Development (Local)

```bash
# 1. Activate virtual environment
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

# 2. Set environment variables
cp .env.example .env
# Edit .env and fill in API_ID, API_HASH, BOT_TOKEN, OWNER_ID, ENCRYPTION_KEY

# 3. Run
python -m bot.main
