
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Structured logger with color + file rotation.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import settings


class ColorFormatter(logging.Formatter):
    """Colored console output for dev."""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[41m",  # Red bg
    }
    RESET = "\033[0m"
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


def setup_logger(name: str = "sessionbot") -> logging.Logger:
    """Configure root logger once."""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger  # Already configured
    
    logger.setLevel(settings.LOG_LEVEL)
    logger.propagate = False
    
    fmt = "%(asctime)s │ %(levelname)s │ %(name)s │ %(message)s"
    datefmt = "%H:%M:%S"
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(ColorFormatter(fmt, datefmt=datefmt))
    logger.addHandler(console)
    
    # File handler (rotating)
    try:
        log_file = settings.LOGS_DIR / "bot.log"
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"File logging disabled: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a child logger."""
    return logging.getLogger(f"sessionbot.{name}")


# Initialize on import
setup_logger()
