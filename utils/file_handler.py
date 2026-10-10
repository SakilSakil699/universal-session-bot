
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

File upload/download handlers — safe paths, size checks.
"""
import io
import zipfile
from pathlib import Path
from typing import Optional

from aiogram.types import Document

from config import settings, Emojis
from utils.validators import Validators


class FileHandler:
    """Safe file operations."""
    
    MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED = {".session", ".json", ".txt", ".zip"}
    
    @staticmethod
    async def download_document(
        bot, document: Document, dest: Path
    ) -> Optional[Path]:
        """
        Download a Telegram document safely.
        Returns path or None if invalid.
        """
        # Size check
        if document.file_size and document.file_size > FileHandler.MAX_SIZE:
            raise ValueError(
                f"File too large ({document.file_size} bytes). "
                f"Max: {FileHandler.MAX_SIZE} bytes"
            )
        
        # Extension check
        filename = document.file_name or "uploaded_file"
        if not Validators.is_allowed_file(filename):
            raise ValueError(f"File type not allowed: {filename}")
        
        # Ensure dest is inside data dir (path traversal protection)
        dest = dest.resolve()
        if not str(dest).startswith(str(settings.DATA_DIR.resolve())):
            raise ValueError("Path traversal detected")
        
        dest.parent.mkdir(parents=True, exist_ok=True)
        await bot.download(document, destination=dest)
        return dest
    
    @staticmethod
    def read_session_file(path: Path) -> str:
        """Read session from .session / .json / .txt."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if path.stat().st_size > FileHandler.MAX_SIZE:
            raise ValueError("File too large")
        
        return path.read_text(encoding="utf-8").strip()
    
    @staticmethod
    def make_zip(files: dict) -> io.BytesIO:
        """
        Create in-memory zip from {filename: content}.
        Content can be str or bytes.
        """
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, content in files.items():
                if isinstance(content, str):
                    content = content.encode("utf-8")
                zf.writestr(name, content)
        buf.seek(0)
        return buf
    
    @staticmethod
    def cleanup(*paths: Path) -> None:
        """Delete files silently."""
        for p in paths:
            try:
                if p and p.exists() and p.is_file():
                    p.unlink()
            except Exception:
                pass
