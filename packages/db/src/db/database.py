"""Database connection and session management."""

from typing import Generator

from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from pyshared.config import settings


def get_engine():
    """Get database engine."""
    return create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_recycle=300,
    )


def get_async_engine() -> AsyncEngine:
    """Get async database engine."""
    async_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    return create_async_engine(
        async_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_recycle=300,
    )


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    engine = get_engine()
    with Session(engine) as session:
        yield session


async def get_async_session() -> AsyncSession:
    """Get async database session."""
    engine = get_async_engine()
    async with AsyncSession(engine) as session:
        yield session


def create_tables():
    """Create all database tables."""
    from .models import BaseModel
    
    engine = get_engine()
    BaseModel.metadata.create_all(engine)


async def create_tables_async():
    """Create all database tables asynchronously."""
    from .models import BaseModel
    
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)