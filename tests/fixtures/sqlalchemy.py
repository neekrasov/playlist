import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from playlist.domain.entities import Playlist, Song
from playlist.adapters.sqlalchemy.models import start_mapping
from playlist.adapters.sqlalchemy.repo import PlaylistRepositoryImpl
from playlist.adapters.sqlalchemy.reader import PlaylistReaderImpl

from playlist.config import Settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def start_mapping_fixture() -> None:
    start_mapping()


@pytest_asyncio.fixture(scope="session")
async def settings() -> Settings:
    return Settings()


@pytest_asyncio.fixture(scope="session")
async def session(settings: Settings, start_mapping_fixture):
    engine = create_async_engine(settings.postgres.url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        yield session
        await session.close()

    await engine.dispose()


@pytest_asyncio.fixture(scope="class")
async def fill_db_data(session: AsyncSession, playlists_id, songs_id):
    playlists = [
        Playlist("title1", playlists_id[0]),
        Playlist("title2", playlists_id[1]),
    ]
    songs = [
        Song(
            "title11",
            100,
            songs_id[0],
            playlists_id[0],
        ),
        Song(
            "title12",
            100,
            songs_id[1],
            playlists_id[0],
        ),
        Song(
            "title13",
            100,
            songs_id[2],
            playlists_id[0],
        ),
        Song(
            "title21",
            100,
            songs_id[3],
            playlists_id[1],
        ),
        Song(
            "title22",
            100,
            songs_id[4],
            playlists_id[1],
        ),
        Song(
            "title23",
            100,
            songs_id[5],
            playlists_id[1],
        ),
    ]
    session.add_all(playlists)
    session.add_all(songs)
    await session.commit()
    yield

    for playlist in playlists:
        await session.delete(playlist)
    await session.commit()


@pytest_asyncio.fixture()
async def playlists_repository(
    session: AsyncSession,
) -> PlaylistRepositoryImpl:
    return PlaylistRepositoryImpl(session)


@pytest_asyncio.fixture()
async def playlists_reader(
    session: AsyncSession,
) -> PlaylistReaderImpl:
    return PlaylistReaderImpl(session)
