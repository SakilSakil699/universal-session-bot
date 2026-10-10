"""
Constants used across the bot.
DC IPs, format names, engine names, UI colors.
"""
from enum import Enum


# ── Telegram Data Centers ────────────────────────
DC_IPS = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}

DC_NAMES = {
    1: "Miami, USA",
    2: "Amsterdam, Netherlands",
    3: "Miami, USA",
    4: "Amsterdam, Netherlands",
    5: "Singapore",
}

DC_PORTS = {1: 443, 2: 443, 3: 443, 4: 443, 5: 443}

# ── Session Formats ──────────────────────────────
class Formats(str, Enum):
    PYROGRAM = "pyrogram"
    TELETHON = "telethon"
    GRAMJS = "gramjs"
    MTCUTE = "mtcute"
    JSON = "json"
    TDATA = "tdata"
    TGNET = "tgnet"
    FEROGRAM = "ferogram"
    AUTH_KEY = "auth_key"


FORMAT_NAMES = {
    Formats.PYROGRAM: "🔹 Pyrogram String",
    Formats.TELETHON: "🔹 Telethon String",
    Formats.GRAMJS: "🔹 GramJS Hex",
    Formats.MTCUTE: "🔹 Mtcute String",
    Formats.JSON: "🔹 JSON",
    Formats.TDATA: "📦 TData (Desktop)",
    Formats.TGNET: "📦 Android tgnet",
    Formats.FEROGRAM: "🦀 Ferogram",
    Formats.AUTH_KEY: "🔑 Auth Key",
}

# ── Login Engines ────────────────────────────────
class Engines(str, Enum):
    TELETHON = "telethon"
    PYROGRAM = "pyrogram"
    FEROGRAM = "ferogram"


ENGINE_NAMES = {
    Engines.TELETHON: "⚡ Telethon (Recommended)",
    Engines.PYROGRAM: "🚀 Pyrogram (Fast)",
    Engines.FEROGRAM: "🦀 Ferogram (Experimental)",
}

# ── Bot Version ──────────────────────────────────
BOT_VERSION = "1.0.0"
BOT_NAME = "Universal Session Bot"

# ── UI Colors (HTML tags for Telegram) ───────────
class Colors:
    """Telegram HTML colors."""
    BOLD = "<b>{}</b>"
    ITALIC = "<i>{}</i>"
    CODE = "<code>{}</code>"
    PRE = "<pre>{}</pre>"
    LINK = '<a href="{}">{}</a>'
    SPOILER = "<tg-spoiler>{}</tg-spoiler>"


# ── Emoji Set (Consistent UI) ────────────────────
class Emojis:
    LOCK = "🔐"
    KEY = "🔑"
    PHONE = "📱"
    OTP = "📩"
    CHECK = "✅"
    CROSS = "❌"
    WARN = "⚠️"
    INFO = "ℹ️"
    ROCKET = "🚀"
    BOLT = "⚡"
    CRAB = "🦀"
    PACKAGE = "📦"
    USER = "👤"
    STATS = "📊"
    SETTINGS = "⚙️"
    HELP = "❓"
    ABOUT = "ℹ️"
    FILE = "📂"
    LOADING = "⏳"
    SUCCESS = "🎉"
    TIME = "⏰"
    SHIELD = "🛡️"
    CROWN = "👑"
    STAR = "⭐"
