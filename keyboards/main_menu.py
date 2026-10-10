
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Main menu, back, and confirmation keyboards.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Emojis


def main_menu_kb() -> InlineKeyboardMarkup:
    """
    Main menu with 2-column grid layout.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{Emojis.LOCK} New Session",
                callback_data="menu_new_session"
            ),
            InlineKeyboardButton(
                text=f"{Emojis.FILE} My Sessions",
                callback_data="menu_my_sessions"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{Emojis.SETTINGS} Settings",
                callback_data="menu_settings"
            ),
            InlineKeyboardButton(
                text=f"{Emojis.STATS} Stats",
                callback_data="menu_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{Emojis.HELP} Help",
                callback_data="menu_help"
            ),
            InlineKeyboardButton(
                text=f"{Emojis.ABOUT} About",
                callback_data="menu_about"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{Emojis.STAR} Credits",
                callback_data="menu_credit"
            ),
        ],
    ])


def back_to_menu_kb() -> InlineKeyboardMarkup:
    """Single back-to-menu button."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{Emojis.SHIELD} Main Menu",
                callback_data="menu_main"
            ),
        ],
    ])


def confirm_kb(action: str) -> InlineKeyboardMarkup:
    """
    Yes/No confirmation dialog.
    action: unique string used in callback_data (e.g. "delete_session_123")
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{Emojis.CHECK} Yes",
                callback_data=f"confirm_{action}"
            ),
            InlineKeyboardButton(
                text=f"{Emojis.CROSS} No",
                callback_data="cancel_action"
            ),
        ],
    ])
