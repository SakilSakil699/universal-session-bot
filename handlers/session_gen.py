"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Session generation flow — phone → OTP → 2FA → format select.
"""
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from config import settings, Author, Emojis
from engines import TelethonEngine, PyrogramEngine
from core import SessionConverter, SessionUtils
from keyboards.engines import engine_kb
from keyboards.formats import format_kb
from utils.validators import Validators

log = logging.getLogger(__name__)
router = Router(name="session_gen")


# ═══════════════════════════════════════════════
#  FSM States
# ═══════════════════════════════════════════════

class SessionFlow(StatesGroup):
    choosing_engine = State()
    phone = State()
    otp = State()
    password = State()
    choosing_format = State()


# ═══════════════════════════════════════════════
#  /newsession — Entry
# ═══════════════════════════════════════════════

@router.message(Command("newsession"))
async def cmd_new_session(msg: Message, state: FSMContext):
    await state.clear()
    text = (
        f"<b>🔐 New Session</b>\n\n"
        f"Step <b>1/4</b> — Choose login engine:\n\n"
        f"⚡ <b>Telethon</b> — Stable, recommended\n"
        f"🚀 <b>Pyrogram</b> — Fast, clean API\n"
        f"🦀 <b>Ferogram</b> — Rust core (experimental)\n\n"
        f"<i>Tip: Start with Telethon if unsure.</i>"
    )
    await msg.answer(text, reply_markup=engine_kb())
    await state.set_state(SessionFlow.choosing_engine)


@router.callback_query(SessionFlow.choosing_engine, F.data.startswith("engine_"))
async def cb_engine(cb: CallbackQuery, state: FSMContext):
    engine = cb.data.replace("engine_", "")
    await state.update_data(engine=engine)
    
    text = (
        f"<b>📱 Step 2/4 — Phone Number</b>\n\n"
        f"Engine: <code>{engine}</code>\n\n"
        f"Send your phone number in international format:\n"
        f"<code>+919876543210</code>\n\n"
        f"⚠️ <b>Rules:</b>\n"
        f"  • Include country code (+91, +1, etc.)\n"
        f"  • No spaces or dashes\n"
        f"  • Use your own number only\n\n"
        f"<i>Type /cancel anytime to abort.</i>"
    )
    await cb.message.edit_text(text)
    await state.set_state(SessionFlow.phone)
    await cb.answer()


# ═══════════════════════════════════════════════
#  Phone input
# ═══════════════════════════════════════════════

@router.message(SessionFlow.phone)
async def got_phone(msg: Message, state: FSMContext):
    phone = msg.text.strip()
    
    if not Validators.is_valid_phone(phone):
        await msg.answer(
            f"{Emojis.CROSS} <b>Invalid phone number</b>\n\n"
            f"Format: <code>+919876543210</code>\n"
            f"Try again or /cancel"
        )
        return
    
    data = await state.get_data()
    engine_name = data["engine"]
    
    loading = await msg.answer(f"{Emojis.LOADING} Sending OTP via <b>{engine_name}</b>...")
    
    try:
        engine = _get_engine(engine_name)
        result = await engine.send_code(phone)
        
        if not result.success:
            await loading.edit_text(f"{Emojis.CROSS} {result.error}")
            return
        
        await state.update_data(
            phone=phone,
            phone_code_hash=result.phone_code_hash,
        )
        
        await loading.edit_text(
            f"<b>📩 Step 3/4 — Enter OTP</b>\n\n"
            f"OTP sent to <code>{phone}</code>\n\n"
            f"<b>⚠️ Important:</b>\n"
            f"Send code with <b>spaces</b> between digits:\n"
            f"<code>1 2 3 4 5</code>\n\n"
            f"<i>Why spaces? Telegram expires codes that look like session strings.</i>\n\n"
            f"{Emojis.TIME} Code expires in 5 minutes\n"
            f"Type /cancel to abort."
        )
        await state.set_state(SessionFlow.otp)
    
    except Exception as e:
        log.error(f"send_code error: {e}")
        await loading.edit_text(f"{Emojis.CROSS} Error: <code>{e}</code>")


# ═══════════════════════════════════════════════
#  OTP input
# ═══════════════════════════════════════════════

@router.message(SessionFlow.otp)
async def got_otp(msg: Message, state: FSMContext):
    code = msg.text.replace(" ", "").strip()
    
    if not Validators.is_valid_otp(code):
        await msg.answer(
            f"{Emojis.CROSS} Invalid OTP. Send 5 digits with spaces:\n"
            f"<code>1 2 3 4 5</code>"
        )
        return
    
    data = await state.get_data()
    loading = await msg.answer(f"{Emojis.LOADING} Verifying OTP...")
    
    try:
        engine = _get_engine(data["engine"])
        result = await engine.verify_code(
            phone=data["phone"],
            code=code,
            phone_code_hash=data["phone_code_hash"],
        )
        
        if result.needs_password:
            await loading.edit_text(
                f"<b>🔑 Step 3.5/4 — 2FA Password</b>\n\n"
                f"Your account has two-factor authentication.\n\n"
                f"Send your 2FA password:\n"
                f"<i>(This message will be deleted automatically)</i>"
            )
            await state.set_state(SessionFlow.password)
            return
        
        if not result.success:
            await loading.edit_text(f"{Emojis.CROSS} {result.error}")
            return
        
        # Success — ask format
        await state.update_data(session=result.session)
        await loading.edit_text(
            f"<b>{Emojis.SUCCESS} Login Successful!</b>\n\n"
            f"{SessionUtils.format_user_info(result.session)}\n\n"
            f"<b>Step 4/4 — Choose output format:</b>",
            reply_markup=format_kb(),
        )
        await state.set_state(SessionFlow.choosing_format)
    
    except Exception as e:
        log.error(f"verify_code error: {e}")
        await loading.edit_text(f"{Emojis.CROSS} Error: <code>{e}</code>")


# ═══════════════════════════════════════════════
#  2FA Password
# ═══════════════════════════════════════════════

@router.message(SessionFlow.password)
async def got_password(msg: Message, state: FSMContext):
    password = msg.text
    # Delete password message immediately
    try:
        await msg.delete()
    except Exception:
        pass
    
    data = await state.get_data()
    loading = await msg.answer(f"{Emojis.LOADING} Verifying 2FA...")
    
    try:
        engine = _get_engine(data["engine"])
        result = await engine.verify_password(phone=data["phone"], password=password)
        
        if not result.success:
            await loading.edit_text(f"{Emojis.CROSS} {result.error}")
            return
        
        await state.update_data(session=result.session)
        await loading.edit_text(
            f"<b>{Emojis.SUCCESS} 2FA Verified!</b>\n\n"
            f"{SessionUtils.format_user_info(result.session)}\n\n"
            f"<b>Step 4/4 — Choose output format:</b>",
            reply_markup=format_kb(),
        )
        await state.set_state(SessionFlow.choosing_format)
    
    except Exception as e:
        log.error(f"verify_password error: {e}")
        await loading.edit_text(f"{Emojis.CROSS} Error: <code>{e}</code>")


# ═══════════════════════════════════════════════
#  Engine factory
# ═══════════════════════════════════════════════

_engine_cache: dict = {}


def _get_engine(name: str):
    """Return (or create) engine instance."""
    if name in _engine_cache:
        return _engine_cache[name]
    
    engines = {
        "telethon": TelethonEngine,
        "pyrogram": PyrogramEngine,
    }
    cls = engines.get(name)
    if not cls:
        raise ValueError(f"Unknown engine: {name}")
    
    inst = cls(api_id=settings.API_ID, api_hash=settings.API_HASH)
    _engine_cache[name] = inst
    return inst


# ═══════════════════════════════════════════════
#  /cancel
# ═══════════════════════════════════════════════

@router.message(Command("cancel"))
async def cmd_cancel(msg: Message, state: FSMContext):
    current = await state.get_state()
    if not current:
        await msg.answer("Nothing to cancel.")
        return
    await state.clear()
    await msg.answer(f"{Emojis.CHECK} Cancelled. Use /newsession to start again.")
