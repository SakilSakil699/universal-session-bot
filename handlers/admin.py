
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Owner-only admin panel — stats, broadcast, management.
"""
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import settings, Author, Emojis, BOT_VERSION

log = logging.getLogger(__name__)
router = Router(name="admin")


# ═══════════════════════════════════════════════
#  /admin — Owner panel
# ═══════════════════════════════════════════════

@router.message(Command("admin"))
async def cmd_admin(msg: Message):
    if not settings.is_owner(msg.from_user.id):
        await msg.answer(f"{Emojis.CROSS} Owner only command.")
        return
    
    text = (
        f"<b>👑 Admin Panel</b>\n\n"
        f"<b>🔖 Bot:</b> v{BOT_VERSION}\n"
        f"<b>👤 Owner:</b> {Author.NAME_LINK}\n\n"
        f"<b>📊 Quick Stats:</b>\n"
        f"  • Users: —\n"
        f"  • Sessions: —\n"
        f"  • Today: —\n\n"
        f"Choose an action:"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Full Stats", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton(text="📜 Logs", callback_data="admin_logs")],
    ])
    
    await msg.answer(text, reply_markup=kb, disable_web_page_preview=True)


@router.callback_query(F.data == "admin_stats")
async def cb_admin_stats(cb: CallbackQuery):
    if not settings.is_owner(cb.from_user.id):
        await cb.answer("Owner only", show_alert=True)
        return
    
    text = (
        f"<b>📊 Bot Statistics</b>\n\n"
        f"<b>👥 Users</b>\n"
        f"  • Total: <code>0</code>\n"
        f"  • Active today: <code>0</code>\n"
        f"  • New today: <code>0</code>\n\n"
        f"<b>🔐 Sessions</b>\n"
        f"  • Total: <code>0</code>\n"
        f"  • Today: <code>0</code>\n"
        f"  • By engine:\n"
        f"      Telethon: <code>0</code>\n"
        f"      Pyrogram: <code>0</code>\n\n"
        f"<i>DB integration coming soon.</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ {Author.REPO_LINK} by {Author.NAME_LINK}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await cb.message.edit_text(text, disable_web_page_preview=True)
    await cb.answer()


@router.callback_query(F.data == "admin_broadcast")
async def cb_admin_broadcast(cb: CallbackQuery):
    if not settings.is_owner(cb.from_user.id):
        await cb.answer("Owner only", show_alert=True)
        return
    await cb.message.edit_text(
        "📢 <b>Broadcast</b>\n\n"
        "<i>Coming soon.</i>\n\n"
        "Command: <code>/broadcast &lt;message&gt;</code>"
    )
    await cb.answer()


@router.callback_query(F.data == "admin_users")
async def cb_admin_users(cb: CallbackQuery):
    if not settings.is_owner(cb.from_user.id):
        await cb.answer("Owner only", show_alert=True)
        return
    await cb.message.edit_text("👥 <b>User list — coming soon.</b>")
    await cb.answer()


@router.callback_query(F.data == "admin_logs")
async def cb_admin_logs(cb: CallbackQuery):
    if not settings.is_owner(cb.from_user.id):
        await cb.answer("Owner only", show_alert=True)
        return
    await cb.message.edit_text("📜 <b>Logs — coming soon.</b>")
    await cb.answer()
