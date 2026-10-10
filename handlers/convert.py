
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Format selection & conversion output with hyperlinked credit.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import settings, Author, Emojis
from core import SessionConverter, SessionUtils
from keyboards.formats import back_to_formats_kb

log = logging.getLogger(__name__)
router = Router(name="convert")


FORMAT_MAP = {
    "fmt_pyrogram": ("Pyrogram", SessionConverter.to_pyrogram),
    "fmt_telethon": ("Telethon", SessionConverter.to_telethon),
    "fmt_gramjs": ("GramJS", SessionConverter.to_gramjs),
    "fmt_mtcute": ("Mtcute", SessionConverter.to_mtcute),
    "fmt_json": ("JSON", SessionConverter.to_json),
    "fmt_auth_key": ("Auth Key", SessionConverter.to_auth_key_string),
}


@router.callback_query(F.data.startswith("fmt_"))
async def cb_format(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    session = data.get("session")
    
    if not session:
        await cb.answer("Session missing. Restart with /newsession", show_alert=True)
        return
    
    fmt_key = cb.data
    
    # ── "All formats" special case ──
    if fmt_key == "fmt_all":
        await _send_all_formats(cb, session)
        return
    
    # ── Single format ──
    if fmt_key not in FORMAT_MAP:
        await cb.answer("Unknown format", show_alert=True)
        return
    
    name, fn = FORMAT_MAP[fmt_key]
    
    try:
        string = fn(session)
    except Exception as e:
        await cb.answer(f"Conversion failed: {e}", show_alert=True)
        return
    
    # Build output text
    text = _build_output(session, name, string)
    
    # Copy button
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Copy Format", callback_data=f"copy_{name.lower()}")],
        [InlineKeyboardButton(text="🔄 Another Format", callback_data="fmt_back")],
    ])
    
    await cb.message.edit_text(
        text,
        reply_markup=kb,
        disable_web_page_preview=True,
    )
    await cb.answer(f"{name} generated ✅")


@router.callback_query(F.data == "fmt_back")
async def cb_back(cb: CallbackQuery):
    from keyboards.formats import format_kb
    await cb.message.edit_text(
        "<b>🔄 Choose another format:</b>",
        reply_markup=format_kb(),
    )
    await cb.answer()


async def _send_all_formats(cb: CallbackQuery, session):
    """Convert to all formats and send."""
    try:
        all_fmts = SessionConverter.convert_all(session)
    except Exception as e:
        await cb.answer(f"Failed: {e}", show_alert=True)
        return
    
    header = (
        f"<b>{Emojis.PACKAGE} All Formats Ready!</b>\n\n"
        f"{SessionUtils.format_user_info(session)}\n"
    )
    
    parts = [header]
    for name, value in all_fmts.items():
        parts.append(
            f"<b>🔹 {name.title()}:</b>\n"
            f"<code>{value}</code>\n"
        )
    
    parts.append(Author.CREDIT_FOOTER)
    full_text = "\n".join(parts)
    
    # Split if too long
    if len(full_text) > 4000:
        await cb.message.edit_text(header)
        for name, value in all_fmts.items():
            await cb.message.answer(
                f"<b>🔹 {name.title()}:</b>\n<code>{value}</code>"
            )
        await cb.message.answer(Author.CREDIT_FOOTER)
    else:
        await cb.message.edit_text(full_text, disable_web_page_preview=True)
    
    await cb.answer("All formats generated ✅")


def _build_output(session, fmt_name: str, string: str) -> str:
    """Build formatted output with credit footer."""
    return (
        f"<b>{Emojis.CHECK} {fmt_name} Session Ready!</b>\n\n"
        f"{SessionUtils.format_user_info(session)}\n\n"
        f"<b>🔐 Session String:</b>\n"
        f"<code>{string}</code>"
        f"\n"
        f"{Author.CREDIT_FOOTER}"
    )


@router.callback_query(F.data.startswith("copy_"))
async def cb_copy(cb: CallbackQuery):
    await cb.answer(
        "💡 Tap the code block to copy it!",
        show_alert=True,
    )
