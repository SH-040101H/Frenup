"""Database connection and session management."""

from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel

from pyshared import settings


# Sync engine and session
engine = create_engine(
    settings.database.database_url,
    echo=settings.database.db_echo,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)

# Async engine and session
async_engine = create_async_engine(
    settings.database.async_database_url,
    echo=settings.database.db_echo,
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency for sync operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session dependency."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await async_engine.dispose()


# Database health check
async def check_db_health() -> bool:
    """Check database health."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False


def check_db_health_sync() -> bool:
    """Check database health (sync)."""
    try:
        with SessionLocal() as session:
            session.execute("SELECT 1")
            return True
    except Exception:
        return False