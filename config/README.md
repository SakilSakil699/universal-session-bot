# Config Module

Universal Session Bot
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH)

Central configuration for the bot.

## Files

| File | Purpose |
|------|---------|
| `settings.py` | Env-based settings, validated at startup |
| `constants.py` | DC IPs, formats, engines, emojis, **Author credit** |

## Author Credit Usage

All credit values are **clickable hyperlinks** in Telegram:

```python
from config.constants import Author

# Session output with credit
message = f"Session: {session_str}\n{Author.CREDIT_FOOTER}"

# About page
await msg.answer(Author.ABOUT_BLOCK)
