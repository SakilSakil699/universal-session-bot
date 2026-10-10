
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Main entry point — initializes bot, dispatcher, routers, middleware.
"""
import asyncio
import sys
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import settings, Author, Emojis, BOT_VERSION, BOT_NAME
from utils import get_logger, setup_logger

# Import handlers (registers routers)
from handlers import start, session_gen, convert, my_sessions, admin

log = get_logger("main")


# ═══════════════════════════════════════════════
#  Bot Commands (Menu)
# ═══════════════════════════════════════════════

async def set_bot_commands(bot: Bot) -> None:
    """Set the command menu shown in Telegram UI."""
    commands = [
        BotCommand(command="start",      description="🏠 Welcome menu"),
        BotCommand(command="newsession", description="🔐 Create new session"),
        BotCommand(command="mysessions", description="📂 View saved sessions"),
        BotCommand(command="help",       description="❓ Help & commands"),
        BotCommand(command="about",      description="ℹ️ About the bot"),
        BotCommand(command="cancel",     description="❌ Cancel current flow"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    log.info("Bot commands menu set")


# ═══════════════════════════════════════════════
#  Dispatcher Setup
# ═══════════════════════════════════════════════

def create_dispatcher() -> Dispatcher:
    """Build dispatcher with routers & FSM storage."""
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers in order
    dp.include_router(start.router)
    dp.include_router(session_gen.router)
    dp.include_router(convert.router)
    dp.include_router(my_sessions.router)
    dp.include_router(admin.router)
    
    log.info(
        f"Routers registered: "
        f"start, session_gen, convert, my_sessions, admin"
    )
    return dp


# ═══════════════════════════════════════════════
#  Startup / Shutdown
# ═══════════════════════════════════════════════

async def on_startup(bot: Bot) -> None:
    """Called when bot starts."""
    me = await bot.get_me()
    
    log.info("=" * 55)
    log.info(f"  {Emojis.LOCK} {BOT_NAME} v{BOT_VERSION}")
    log.info(f"  Author : {Author.NAME} ({Author.USERNAME})")
    log.info(f"  Repo   : {Author.GITHUB_URL}")
    log.info("=" * 55)
    log.info(f"Bot ID   : {me.id}")
    log.info(f"Username : @{me.username}")
    log.info(f"Owner    : {settings.OWNER_ID}")
    log.info("=" * 55)
    
    # Set command menu
    await set_bot_commands(bot)
    
    # Notify owner
    try:
        await bot.send_message(
            settings.OWNER_ID,
            f"{Emojis.ROCKET} <b>Bot Started!</b>\n\n"
            f"🤖 <b>{BOT_NAME}</b> v{BOT_VERSION}\n"
            f"🆔 <code>{me.id}</code>\n"
            f"🔗 @{me.username}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💻 {Author.NAME_LINK}\n"
            f"📢 {Author.USERNAME_LINK}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        log.info("Owner notified")
    except Exception as e:
        log.warning(f"Could not notify owner: {e}")


async def on_shutdown(bot: Bot) -> None:
    """Called when bot stops."""
    log.info("Shutting down...")
    
    # Cleanup engine temp clients
    try:
        from handlers.session_gen import _engine_cache
        for engine in _engine_cache.values():
            with suppress(Exception):
                await engine.cleanup()
        log.info("Engines cleaned up")
    except Exception as e:
        log.warning(f"Engine cleanup: {e}")
    
    log.info("Goodbye 👋")


# ═══════════════════════════════════════════════
#  Main Entry Point
# ═══════════════════════════════════════════════

async def main() -> None:
    """Initialize & run bot."""
    
    # Setup logging first
    setup_logger()
    
    # Validate config
    try:
        settings.validate()
        log.info("Config validated ✅")
    except Exception as e:
        log.critical(f"Config validation failed: {e}")
        sys.exit(1)
    
    # Create bot with custom session
    session = AiohttpSession(timeout=30)
    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )
    
    # Verify bot token
    try:
        me = await bot.get_me()
        log.info(f"Bot authenticated: @{me.username}")
    except TelegramUnauthorizedError:
        log.critical("❌ Invalid BOT_TOKEN. Get a new one from @BotFather.")
        sys.exit(1)
    except Exception as e:
        log.critical(f"❌ Bot auth failed: {e}")
        sys.exit(1)
    
    # Create dispatcher
    dp = create_dispatcher()
    
    # Register lifecycle hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    try:
        log.info("Starting polling...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
    finally:
        await bot.session.close()
        log.info("Session closed")


# ═══════════════════════════════════════════════
#  Run
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    # Install uvloop for speed (Linux/Mac only)
    try:
        import uvloop
        uvloop.install()
        print(f"{Emojis.BOLT} uvloop installed (2-4x faster)")
    except ImportError:
        pass
    
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(f"\n{Emojis.CHECK} Bot stopped gracefully")
