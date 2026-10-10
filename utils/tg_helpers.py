
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Telegram-specific helper functions.
Mention parsing, user info, safe edits, message splitting.
"""
import re
from typing import Optional, List
from aiogram.types import Message, User, CallbackQuery

from config import Author, Emojis
from utils.validators import Validators


class TGHelpers:
    """Stateless Telegram helpers."""
    
    # ═══════════════════════════════════════════════
    #  User Info
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def user_mention(user: User, html: bool = True) -> str:
        """
        Generate a clickable user mention.
        """
        name = user.first_name or "User"
        if html:
            return f'<a href="tg://user?id={user.id}">{name}</a>'
        return f"[{name}](tg://user?id={user.id})"
    
    @staticmethod
    def user_display(user: User) -> str:
        """Format: Sakil (@username) [123456]"""
        parts = [user.first_name or "Unknown"]
        if user.username:
            parts.append(f"(@{user.username})")
        parts.append(f"[<code>{user.id}</code>]")
        return " ".join(parts)
    
    @staticmethod
    def is_same_user(a: User, b: User) -> bool:
        return a.id == b.id
    
    # ═══════════════════════════════════════════════
    #  Message Helpers
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def split_message(text: str, max_len: int = 4000) -> List[str]:
        """
        Split long message into Telegram-safe chunks.
        Preserves HTML tags at line boundaries.
        """
        if len(text) <= max_len:
            return [text]
        
        parts = []
        current = ""
        
        for line in text.split("\n"):
            if len(current) + len(line) + 1 > max_len:
                if current:
                    parts.append(current.rstrip())
                current = line + "\n"
            else:
                current += line + "\n"
        
        if current.strip():
            parts.append(current.rstrip())
        
        return parts
    
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special chars for Telegram."""
        return (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
    
    @staticmethod
    def extract_command_args(message: Message) -> Optional[str]:
        """Extract args after /command."""
        text = message.text or ""
        if " " not in text:
            return None
        return text.split(" ", 1)[1].strip()
    
    @staticmethod
    def is_command(message: Message, command: str) -> bool:
        """Check if message is a specific command."""
        if not message.text:
            return False
        return message.text.split()[0].lower() == f"/{command}".lower()
    
    # ═══════════════════════════════════════════════
    #  Safe Edit / Reply
    # ═══════════════════════════════════════════════
    
    @staticmethod
    async def safe_edit(
        message: Message, text: str,
        reply_markup=None,
        disable_preview: bool = True,
    ) -> bool:
        """
        Edit message, ignoring 'message is not modified' errors.
        Returns True if edited (or same), False on other errors.
        """
        try:
            await message.edit_text(
                text,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_preview,
            )
            return True
        except Exception as e:
            err = str(e).lower()
            if "message is not modified" in err:
                return True  # Same content, no-op
            return False
    
    @staticmethod
    async def safe_delete(message: Message) -> bool:
        """Delete message, ignoring errors."""
        try:
            await message.delete()
            return True
        except Exception:
            return False
    
    # ═══════════════════════════════════════════════
    #  Loading Animation
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def loading_text(step: str = "Processing") -> str:
        """Standard loading message."""
        return f"{Emojis.LOADING} <b>{step}...</b>"
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 10) -> str:
        """Text progress bar: ▓▓▓▓░░░░░░ 40%"""
        if total <= 0:
            return "░" * width
        filled = int(width * current / total)
        filled = max(0, min(width, filled))
        bar = "▓" * filled + "░" * (width - filled)
        pct = int(100 * current / total)
        return f"{bar} {pct}%"
    
    # ═══════════════════════════════════════════════
    #  Session Output Formatting
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def format_session_output(
        session_name: str,
        session_string: str,
        extra_info: str = None,
    ) -> str:
        """
        Standard session output with credit footer.
        """
        parts = [
            f"<b>{Emojis.CHECK} {session_name} Session Ready!</b>\n",
        ]
        if extra_info:
            parts.append(extra_info + "\n")
        parts.append(f"<b>{Emojis.LOCK} Session String:</b>")
        parts.append(f"<code>{session_string}</code>")
        parts.append(Author.CREDIT_FOOTER)
        return "\n".join(parts)
    
    @staticmethod
    def format_error(error: str) -> str:
        """Standard error format."""
        return f"{Emojis.CROSS} <b>Error:</b> <code>{TGHelpers.escape_html(error)}</code>"
    
    @staticmethod
    def format_success(msg: str) -> str:
        return f"{Emojis.CHECK} <b>{msg}</b>"
    
    @staticmethod
    def format_warning(msg: str) -> str:
        return f"{Emojis.WARN} <b>{msg}</b>"
    
    @staticmethod
    def format_info(msg: str) -> str:
        return f"{Emojis.INFO} {msg}"
    
    # ═══════════════════════════════════════════════
    #  Masking (for safe logging)
    # ═══════════════════════════════════════════════
    
    @staticmethod
    def mask_session(session_str: str, show: int = 15) -> str:
        """Mask session string for safe display."""
        if len(session_str) <= show * 2:
            return session_str[:show] + "***"
        return f"{session_str[:show]}...{session_str[-show:]}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Delegate to Validators."""
        return Validators.mask_phone(phone)
    
    # ═══════════════════════════════════════════════
    #  Callback Helpers
    # ═══════════════════════════════════════════════
    
    @staticmethod
    async def answer_callback(
        cb: CallbackQuery,
        text: str = None,
        alert: bool = False,
    ) -> None:
        """Safe callback answer."""
        try:
            await cb.answer(text=text, show_alert=alert)
        except Exception:
            pass
    
    @staticmethod
    def parse_callback(cb_data: str, prefix: str) -> Optional[str]:
        """
        Extract value after prefix.
        'fmt_pyrogram' + prefix='fmt_' → 'pyrogram'
        """
        if not cb_data.startswith(prefix):
            return None
        return cb_data[len(prefix):]
