"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Session metadata endpoints.
IMPORTANT: This NEVER exposes decrypted session content.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from db import db, crud
from utils import get_logger
from .stats import require_admin

log = get_logger("api.sessions")
router = APIRouter()


@router.get("/sessions", summary="List sessions (metadata only)")
async def list_sessions(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    limit: int = Query(50, ge=1, le=500),
    _=Depends(require_admin),
):
    """
    List session metadata.
    **Never** returns decrypted auth_key or session string.
    """
    async with db.session() as s:
        if user_id:
            sessions = await crud.list_user_sessions(s, user_id=user_id)
        else:
            from sqlalchemy import select
            from db.models import Session
            result = await s.execute(
                select(Session).order_by(Session.created_at.desc()).limit(limit)
            )
            sessions = list(result.scalars().all())

    return {
        "count": len(sessions),
        "sessions": [
            {
                "id": sess.id,
                "user_id": sess.user_id,
                "engine": sess.engine,
                "dc_id": sess.dc_id,
                "tg_user_id": sess.tg_user_id,
                "phone": sess.phone,
                "first_name": sess.first_name,
                "username": sess.username,
                "is_bot": sess.is_bot,
                "fingerprint": sess.fingerprint,
                "is_active": sess.is_active,
                "created_at": sess.created_at.isoformat(),
            }
            for sess in sessions
        ],
    }


@router.get("/sessions/{session_id}", summary="Get single session metadata")
async def get_session(
    session_id: int,
    _=Depends(require_admin),
):
    async with db.session() as s:
        from sqlalchemy import select
        from db.models import Session
        result = await s.execute(
            select(Session).where(Session.id == session_id)
        )
        sess = result.scalar_one_or_none()

    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "id": sess.id,
        "user_id": sess.user_id,
        "engine": sess.engine,
        "dc_id": sess.dc_id,
        "tg_user_id": sess.tg_user_id,
        "phone": sess.phone,
        "first_name": sess.first_name,
        "username": sess.username,
        "is_bot": sess.is_bot,
        "fingerprint": sess.fingerprint,
        "is_active": sess.is_active,
        "created_at": sess.created_at.isoformat(),
    }


@router.delete("/sessions/{session_id}", summary="Delete session")
async def delete_session(
    session_id: int,
    _=Depends(require_admin),
):
    async with db.session() as s:
        from sqlalchemy import delete
        from db.models import Session
        result = await s.execute(
            delete(Session).where(Session.id == session_id)
        )
        await s.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"status": "deleted", "id": session_id}
