
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Async PostgreSQL/SQLite engine + session factory.
"""
import logging
from typing import Optional, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from config import settings

log = logging.getLogger(__name__)


class Database:
    """
    Async database manager.
    Singleton pattern — use module-level `db` instance.
    """

    def __init__(self, url: Optional[str] = None):
        self.url = url or settings.DATABASE_URL
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None

    async def init(self) -> None:
        """Create engine, session factory, and tables."""
        # SQLite special handling
        connect_args = {}
        if self.url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        self._engine = create_async_engine(
            self.url,
            echo=False,
            pool_pre_ping=True,
            connect_args=connect_args,
        )

        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        # Create tables
        from .models import Base
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        log.info(f"Database ready: {self.url.split('@')[-1]}")

    async def close(self) -> None:
        """Dispose engine."""
        if self._engine:
            await self._engine.dispose()
            log.info("Database closed")

    def session(self) -> AsyncSession:
        """Get a new session (caller must close)."""
        if not self._session_factory:
            raise RuntimeError("Database not initialized. Call await db.init()")
        return self._session_factory()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Dependency for FastAPI or use in `async with db.session() as s:`.
        """
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


# ── Module-level singleton ──────────────────────
db = Database()
