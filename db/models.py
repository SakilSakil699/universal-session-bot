
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

SQLAlchemy models — User, Session, ActivityLog.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger, String, Integer, Boolean,
    DateTime, Text, ForeignKey, Index,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


# ═══════════════════════════════════════════════
#  User
# ═══════════════════════════════════════════════

class User(Base):
    """Bot user (Telegram account holder)."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Stats
    session_count: Mapped[int] = mapped_column(Integer, default=0)
    last_active: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relations
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    logs: Mapped[list["ActivityLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} @{self.username}>"


# ═══════════════════════════════════════════════
#  Session
# ═══════════════════════════════════════════════

class Session(Base):
    """
    Encrypted Telegram session.
    `encrypted_data` = AES-256-GCM blob (base64).
    NEVER store plaintext auth_key.
    """
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    # Metadata (safe to show)
    label: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    engine: Mapped[str] = mapped_column(String(16))     # telethon/pyrogram/ferogram
    dc_id: Mapped[int] = mapped_column(Integer)
    tg_user_id: Mapped[int] = mapped_column(BigInteger)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)

    # Encrypted payload (base64)
    encrypted_data: Mapped[str] = mapped_column(Text)
    fingerprint: Mapped[str] = mapped_column(String(16), index=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relations
    user: Mapped["User"] = relationship(back_populates="sessions")

    __table_args__ = (
        Index("ix_sessions_user_fingerprint", "user_id", "fingerprint"),
    )

    def __repr__(self) -> str:
        return f"<Session id={self.id} engine={self.engine} dc={self.dc_id}>"


# ═══════════════════════════════════════════════
#  ActivityLog
# ═══════════════════════════════════════════════

class ActivityLog(Base):
    """Audit trail — track actions for debugging & security."""
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    action: Mapped[str] = mapped_column(String(32), index=True)
    detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    user: Mapped["User"] = relationship(back_populates="logs")

    def __repr__(self) -> str:
        return f"<ActivityLog {self.action} user={self.user_id}>"
