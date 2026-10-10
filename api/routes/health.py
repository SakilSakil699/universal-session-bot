"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Health check endpoints.
"""
from datetime import datetime

from fastapi import APIRouter

from config import Author, BOT_VERSION

router = APIRouter()


@router.get("/health", summary="Health check")
async def health():
    """Simple health check — returns OK if API is up."""
    return {
        "status": "ok",
        "version": BOT_VERSION,
        "time": datetime.utcnow().isoformat(),
        "author": Author.NAME,
        "telegram": Author.TELEGRAM_URL,
    }


@router.get("/health/deep", summary="Deep health check")
async def health_deep():
    """Deep check — verifies DB & Redis connectivity."""
    from db import db
    from sqlalchemy import text

    result = {
        "status": "ok",
        "checks": {},
    }

    # DB
    try:
        async with db.session() as s:
            await s.execute(text("SELECT 1"))
        result["checks"]["database"] = "ok"
    except Exception as e:
        result["checks"]["database"] = f"error: {e}"
        result["status"] = "degraded"

    # Redis (optional)
    try:
        import redis.asyncio as aioredis
        from config import settings
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.close()
        result["checks"]["redis"] = "ok"
    except Exception as e:
        result["checks"]["redis"] = f"unavailable: {e}"

    return result
