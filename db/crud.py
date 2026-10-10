
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

CRUD operations — Create, Read, Update, Delete.
"""
from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Session, ActivityLog
from core.universal_session import UniversalSession
from core.session_utils import SessionUtils


# ═══════════════════════════════════════════════
#  Users
# ═══════════════════════════════════════════════

async def get_or_create_user(
    s: AsyncSession, tg_user_id: int,
    username: str = None, first_name: str = None,
    last_name: str = None, language_code: str = None,
) -> User:
    """Fetch user or create if not exists."""
    user = await s.get(User, tg_user_id)
    if user:
        # Update fields
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if language_code is not None:
            user.language_code = language_code
        user.last_active = datetime.utcnow()
    else:
        user = User(
            id=tg_user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
        )
        s.add(user)
    await s.flush()
    return user


async def get_user(s: AsyncSession, user_id: int) -> Optional[User]:
    return await s.get(User, user_id)


async def ban_user(s: AsyncSession, user_id: int, banned: bool = True) -> bool:
    user = await s.get(User, user_id)
    if not user:
        return False
    user.is_banned = banned
    await s.flush()
    return True


# ═══════════════════════════════════════════════
#  Sessions
# ═══════════════════════════════════════════════

async def save_session(
    s: AsyncSession,
    user_id: int,
    session: UniversalSession,
    encrypted_data: str,
    engine: str,
    label: str = None,
) -> Session:
    """
    Save encrypted session to DB.
    Checks for duplicates by fingerprint.
    """
    fingerprint = SessionUtils.auth_key_fingerprint(session.auth_key)

    # Dedup check
    existing = await s.execute(
        select(Session).where(
            Session.user_id == user_id,
            Session.fingerprint == fingerprint,
        )
    )
    existing = existing.scalar_one_or_none()
    if existing:
        existing.is_active = True
        existing.encrypted_data = encrypted_data
        await s.flush()
        return existing

    row = Session(
        user_id=user_id,
        engine=engine,
        dc_id=session.dc_id,
        tg_user_id=session.user_id,
        phone=session.phone,
        first_name=session.first_name,
        username=session.username,
        is_bot=session.is_bot,
        encrypted_data=encrypted_data,
        fingerprint=fingerprint,
        label=label,
    )
    s.add(row)

    # Update user's session count
    user = await s.get(User, user_id)
    if user:
        user.session_count += 1

    await s.flush()
    return row


async def list_user_sessions(
    s: AsyncSession, user_id: int, active_only: bool = True
) -> List[Session]:
    q = select(Session).where(Session.user_id == user_id)
    if active_only:
        q = q.where(Session.is_active == True)
    q = q.order_by(Session.created_at.desc())
    result = await s.execute(q)
    return list(result.scalars().all())


async def get_session(
    s: AsyncSession, session_id: int, user_id: int
) -> Optional[Session]:
    q = select(Session).where(
        Session.id == session_id,
        Session.user_id == user_id,
    )
    result = await s.execute(q)
    return result.scalar_one_or_none()


async def delete_session(
    s: AsyncSession, session_id: int, user_id: int
) -> bool:
    q = delete(Session).where(
        Session.id == session_id,
        Session.user_id == user_id,
    )
    result = await s.execute(q)
    await s.flush()
    return result.rowcount > 0


async def count_user_sessions(s: AsyncSession, user_id: int) -> int:
    q = select(func.count()).select_from(Session).where(
        Session.user_id == user_id,
        Session.is_active == True,
    )
    result = await s.execute(q)
    return result.scalar() or 0


# ═══════════════════════════════════════════════
#  Activity Logs
# ═══════════════════════════════════════════════

async def log_activity(
    s: AsyncSession,
    user_id: int,
    action: str,
    detail: str = None,
    success: bool = True,
    ip: str = None,
) -> ActivityLog:
    row = ActivityLog(
        user_id=user_id,
        action=action,
        detail=detail,
        success=success,
        ip=ip,
    )
    s.add(row)
    await s.flush()
    return row


async def recent_logs(
    s: AsyncSession, limit: int = 50
) -> List[ActivityLog]:
    q = select(ActivityLog).order_by(
        ActivityLog.created_at.desc()
    ).limit(limit)
    result = await s.execute(q)
    return list(result.scalars().all())


# ═══════════════════════════════════════════════
#  Stats
# ═══════════════════════════════════════════════

async def get_stats(s: AsyncSession) -> dict:
    """Aggregate bot statistics."""
    total_users = (await s.execute(
        select(func.count()).select_from(User)
    )).scalar() or 0

    today = datetime.utcnow() - timedelta(days=1)
    active_today = (await s.execute(
        select(func.count()).select_from(User).where(User.last_active >= today)
    )).scalar() or 0

    total_sessions = (await s.execute(
        select(func.count()).select_from(Session).where(Session.is_active == True)
    )).scalar() or 0

    sessions_today = (await s.execute(
        select(func.count()).select_from(Session).where(Session.created_at >= today)
    )).scalar() or 0

    return {
        "total_users": total_users,
        "active_today": active_today,
        "total_sessions": total_sessions,
        "sessions_today": sessions_today,
    }
