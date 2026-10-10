
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Vendors package — external libraries for session conversion.
Self-contained so bot works even if upstream repos disappear.
"""
from pathlib import Path

VENDORS_DIR = Path(__file__).resolve().parent

__version__ = "1.0.0"
__author__ = "Sakil"
__author_username__ = "@YO_UR_OFFICIAL_CRUSH"
__author_url__ = "https://t.me/YO_UR_OFFICIAL_CRUSH"
__github__ = "https://github.com/SakilSakil699"


def vendor_available(name: str) -> bool:
    """Check if a vendor library is present."""
    return (VENDORS_DIR / name).exists() and (
        (VENDORS_DIR / name).is_dir()
    )


def list_vendors() -> list[str]:
    """List all vendor names currently present."""
    if not VENDORS_DIR.exists():
        return []
    return sorted([
        d.name for d in VENDORS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
    ])


__all__ = [
    "vendor_available",
    "list_vendors",
    "VENDORS_DIR",
    "__version__",
    "__author__",
    "__author_username__",
    "__author_url__",
    "__github__",
]
