
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Format selection keyboard.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings, Emojis


def format_kb() -> InlineKeyboardMarkup:
    """
    Format selection keyboard.
    Optional formats hide if disabled in settings.
    """
    rows = [
        [
            InlineKeyboardButton(
                text="🔹 Pyrogram String",
                callback_data="fmt_pyrogram"
            ),
            InlineKeyboardButton(
                text="🔹 Telethon String",
                callback_data="fmt_telethon"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔹 GramJS Hex",
                callback_data="fmt_gramjs"
            ),
            InlineKeyboardButton(
                text="🔹 Mtcute",
                callback_data="fmt_mtcute"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔹 JSON",
                callback_data="fmt_json"
            ),
            InlineKeyboardButton(
                text="🔑 Auth Key",
                callback_data="fmt_auth_key"
            ),
        ],
    ]
    
    # Optional formats
    optional = []
    if settings.ENABLE_TDATA:
        optional.append(
            InlineKeyboardButton(
                text=f"{Emojis.PACKAGE} TData",
                callback_data="fmt_tdata"
            )
        )
    if settings.ENABLE_TDATA:  # tgnet tied to tdata flag by default
        optional.append(
            InlineKeyboardButton(
                text=f"{Emojis.PACKAGE} tgnet",
                callback_data="fmt_tgnet"
            )
        )
    
    if optional:
        rows.append(optional)
    
    # All formats
    rows.append([
        InlineKeyboardButton(
            text=f"{Emojis.PACKAGE} All Formats",
            callback_data="fmt_all"
        ),
    ])
    
    # Cancel
    rows.append([
        InlineKeyboardButton(
            text=f"{Emojis.CROSS} Cancel",
            callback_data="cancel_action"
        ),
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_to_formats_kb() -> InlineKeyboardMarkup:
    """Back to format selection."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Another Format",
                callback_data="fmt_back"
            ),
        ],
    ])
