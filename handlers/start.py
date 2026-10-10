
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

/start, /help, /about handlers with hyperlinked credit.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import settings, Author, Emojis, BOT_VERSION, BOT_NAME
from keyboards.main_menu import main_menu_kb, back_to_menu_kb

router = Router(name="start")


# ═══════════════════════════════════════════════
#  /start
# ═══════════════════════════════════════════════

@router.message(Command("start"))
async def cmd_start(msg: Message):
    """Welcome message with clickable author credit."""
    user = msg.from_user
    name = user.first_name or "Friend"
    
    text = (
        f"<b>🔐 {BOT_NAME}</b>\n"
        f"<i>Advanced · Secure · Lightning Fast</i>\n\n"
        f"👋 Welcome, <b>{name}</b>!\n\n"
        f"<b>✨ What I can do:</b>\n"
        f"  • Generate Telegram sessions\n"
        f"  • Convert between 9+ formats\n"
        f"  • Encrypt & store securely\n"
        f"  • Real-time account info\n\n"
        f"<b>📦 Supported Formats:</b>\n"
        f"  Pyrogram · Telethon · GramJS · Mtcute\n"
        f"  JSON · TData · tgnet · Ferogram\n\n"
        f"<b>🚀 Quick Start:</b>\n"
        f"  Press <b>🔐 New Session</b> below\n"
        f"\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 Developed by {Author.NAME_LINK}\n"
        f"📢 {Author.USERNAME_LINK} · ⭐ {Author.GITHUB_LINK}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    await msg.answer(text, reply_markup=main_menu_kb(), disable_web_page_preview=True)


# ═══════════════════════════════════════════════
#  /help
# ═══════════════════════════════════════════════

@router.message(Command("help"))
async def cmd_help(msg: Message):
    text = (
        f"<b>❓ Help & Commands</b>\n\n"
        f"<b>🔐 Session Commands:</b>\n"
        f"  /newsession — Create new session\n"
        f"  /mysessions — View saved sessions\n"
        f"  /convert — Convert existing session\n"
        f"  /cancel — Cancel current flow\n\n"
        f"<b>ℹ️ Info Commands:</b>\n"
        f"  /start — Welcome menu\n"
        f"  /help — This message\n"
        f"  /about — About the bot\n"
        f"  /stats — Your usage stats\n\n"
        f"<b>🛡️ Safety Tips:</b>\n"
        f"  • Never share session strings publicly\n"
        f"  • Only use your own accounts\n"
        f"  • Sessions are encrypted at rest\n"
        f"  • OTP expires in 5 minutes\n\n"
        f"<b>💡 Pro Tip:</b>\n"
        f"  Use <b>Telethon</b> engine for stability,\n"
        f"  <b>Pyrogram</b> for speed.\n"
        f"\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ {Author.REPO_LINK} by {Author.NAME_LINK}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await msg.answer(text, reply_markup=back_to_menu_kb(), disable_web_page_preview=True)


# ═══════════════════════════════════════════════
#  /about
# ═══════════════════════════════════════════════

@router.message(Command("about"))
async def cmd_about(msg: Message):
    text = (
        f"<b>ℹ️ About {BOT_NAME}</b>\n\n"
        f"<b>🔖 Version:</b> <code>v{BOT_VERSION}</code>\n"
        f"<b>🐍 Python:</b> 3.10+\n"
        f"<b>🤖 Framework:</b> aiogram 3.x\n"
        f"<b>🔐 Crypto:</b> AES-256-GCM + Argon2id\n"
        f"<b>⚡ Engines:</b> Telethon · Pyrogram · Ferogram\n\n"
        f"<b>✨ Features:</b>\n"
        f"  ✅ 9+ session formats\n"
        f"  ✅ Auto format detection\n"
        f"  ✅ Zero-knowledge encryption\n"
        f"  ✅ Rate limiting & anti-flood\n"
        f"  ✅ Multi-engine login\n"
        f"  ✅ Live account info\n\n"
        f"<b>👨‍💻 Developer:</b> {Author.NAME_LINK}\n"
        f"<b>📢 Telegram:</b> {Author.USERNAME_LINK}\n"
        f"<b>⭐ GitHub:</b> {Author.GITHUB_LINK}\n"
        f"<b>📦 Repo:</b> {Author.REPO_LINK}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"❤️ Made with love by {Author.NAME_LINK}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await msg.answer(text, reply_markup=back_to_menu_kb(), disable_web_page_preview=True)


# ═══════════════════════════════════════════════
#  Callback handlers
# ═══════════════════════════════════════════════

@router.callback_query(F.data == "menu_main")
async def cb_main_menu(cb: CallbackQuery):
    name = cb.from_user.first_name or "Friend"
    text = (
        f"<b>🏠 Main Menu</b>\n\n"
        f"Welcome back, <b>{name}</b>!\n\n"
        f"Choose an option below:"
    )
    await cb.message.edit_text(
        text, reply_markup=main_menu_kb(), disable_web_page_preview=True
    )
    await cb.answer()


@router.callback_query(F.data == "menu_help")
async def cb_help(cb: CallbackQuery):
    await cmd_help(cb.message)
    await cb.answer()


@router.callback_query(F.data == "menu_about")
async def cb_about(cb: CallbackQuery):
    await cmd_about(cb.message)
    await cb.answer()


@router.callback_query(F.data == "menu_credit")
async def cb_credit(cb: CallbackQuery):
    text = (
        f"<b>👨‍💻 Credits</b>\n\n"
        f"<b>Developer:</b> {Author.NAME_LINK}\n"
        f"<b>Telegram:</b> {Author.USERNAME_LINK}\n"
        f"<b>GitHub:</b> {Author.GITHUB_LINK}\n"
        f"<b>Repo:</b> {Author.REPO_LINK}\n\n"
        f"<b>🛠️ Tech Stack:</b>\n"
        f"  • aiogram 3.x\n"
        f"  • Telethon · Pyrogram · Ferogram\n"
        f"  • PostgreSQL · Redis\n"
        f"  • AES-256-GCM encryption\n"
        f"  • Argon2id KDF\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⭐ Star the repo if you like it!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await cb.message.edit_text(
        text, reply_markup=back_to_menu_kb(), disable_web_page_preview=True
    )
    await cb.answer()
