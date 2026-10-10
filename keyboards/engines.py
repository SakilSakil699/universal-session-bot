
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Engine selection keyboard.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings, Emojis


def engine_kb() -> InlineKeyboardMarkup:
    """
    Engine selection keyboard.
    Ferogram button only shows if ENABLE_FEROGRAM=true.
    """
    rows = [
        [
            InlineKeyboardButton(
                text=f"{Emojis.BOLT} Telethon (Recommended)",
                callback_data="engine_telethon"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{Emojis.ROCKET} Pyrogram (Fast)",
                callback_data="engine_pyrogram"
            ),
        ],
    ]
    
    # Optional: Ferogram
    if settings.ENABLE_FEROGRAM:
        rows.append([
            InlineKeyboardButton(
                text=f"{Emojis.CRAB} Ferogram (Experimental)",
                callback_data="engine_ferogram"
            ),
        ])
    
    rows.append([
        InlineKeyboardButton(
            text=f"{Emojis.CROSS} Cancel",
            callback_data="cancel_action"
        ),
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)
