"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Stats endpoints.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import settings, Author, BOT_VERSION
from db import db, crud
from utils import get_logger

log = get_logger("api.stats")
router = APIRouter()
security = HTTPBearer(auto_error=False)


async def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Simple bearer token check."""
    if not credentials or credentials.credentials != settings.ENCRYPTION_KEY[:32]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@router.get("/stats", summary="Bot statistics")
async def get_stats(_=Depends(require_admin)):
    """Aggregated bot statistics."""
    async with db.session() as s:
        stats = await crud.get_stats(s)

    return {
        "bot": {
            "name": "Universal Session Bot",
            "version": BOT_VERSION,
            "author": Author.NAME,
            "telegram": Author.TELEGRAM_URL,
            "github": Author.GITHUB_URL,
        },
        "stats": stats,
        "time": datetime.utcnow().isoformat(),
    }


@router.get("/stats/public", summary="Public stats (no auth)")
async def get_stats_public():
    """Public stats — safe subset."""
    async with db.session() as s:
        stats = await crud.get_stats(s)

    return {
        "total_users": stats["total_users"],
        "total_sessions": stats["total_sessions"],
        "author": Author.NAME,
        "repo": Author.REPO_URL,
    }
