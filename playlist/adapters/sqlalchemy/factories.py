from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from playlist.config import Settings


async def build_sa_engine(
    settings: Settings,
) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(settings.postgres.url)

    yield engine

    await engine.dispose()


def build_sa_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
