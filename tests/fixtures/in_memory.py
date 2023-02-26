import pytest
import uuid
import datetime
from typing import Dict, List
from playlist.domain.entities import Playlist, PlaylistID, Song, SongID
from playlist.adapters.memory.repo import (
    InMemoryPlaylistRepository,
)
from playlist.adapters.memory.cache import InMemoryPlaylistCache
from playlist.adapters.memory.fake_uow import FakeUnitOfWork
from playlist.adapters.memory.reader import InMemoryPlaylistReader


def add_songs_to_playlist(playlist: Playlist, songs: List[Song]) -> None:
    for song in songs:
        song.timestamp = datetime.datetime.now()
        playlist.add_song(song)


@pytest.fixture(scope="class")
def playlists_id() -> tuple[PlaylistID, PlaylistID]:
    return PlaylistID(uuid.uuid4()), PlaylistID(uuid.uuid4())


@pytest.fixture(scope="class")
def playlists() -> Dict[PlaylistID, Playlist]:
    return {}


@pytest.fixture(scope="class")
def songs_id() -> List[SongID]:
    return [
        SongID(uuid.uuid4()),
        SongID(uuid.uuid4()),
        SongID(uuid.uuid4()),
        SongID(uuid.uuid4()),
        SongID(uuid.uuid4()),
        SongID(uuid.uuid4()),
    ]


@pytest.fixture(scope="class")
def songs(songs_id) -> List[Song]:
    return [Song("song", 10, i) for i in songs_id]


@pytest.fixture(scope="class")
def cache_playlists_data() -> Dict[PlaylistID, Playlist]:
    return {}


@pytest.fixture(scope="class")
def filled_cache_playlists_data(
    playlists_id, songs
) -> Dict[PlaylistID, Playlist]:
    playlist_1 = Playlist(
        id=PlaylistID(playlists_id[0]),
        title="Cached Playlist 1",
    )
    playlist_2 = Playlist(
        id=PlaylistID(playlists_id[1]),
        title="Cached Playlist 2",
    )

    add_songs_to_playlist(playlist_1, songs)
    add_songs_to_playlist(playlist_2, songs)
    return {
        PlaylistID(playlists_id[0]): playlist_1,
        PlaylistID(playlists_id[1]): playlist_2,
    }


@pytest.fixture(scope="class")
def filled_playlists(playlists_id, songs) -> Dict[PlaylistID, Playlist]:
    playlist_1 = Playlist(
        id=PlaylistID(playlists_id[0]),
        title="Playlist 1",
    )
    playlist_2 = Playlist(
        id=PlaylistID(playlists_id[1]),
        title="Playlist 2",
    )
    playlist_3 = Playlist(
        id=PlaylistID(playlists_id[1]),
        title="Playlist 3",
    )

    add_songs_to_playlist(playlist_1, songs)
    add_songs_to_playlist(playlist_2, songs)
    add_songs_to_playlist(playlist_3, songs)
    return {
        PlaylistID(playlists_id[0]): playlist_1,
        PlaylistID(playlists_id[1]): playlist_2,
        PlaylistID(playlists_id[1]): playlist_3,
    }


@pytest.fixture(scope="class")
def fake_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture()
def playlists_cache(
    cache_playlists_data: Dict[PlaylistID, Playlist]
) -> InMemoryPlaylistCache:
    return InMemoryPlaylistCache(cache_playlists_data)


@pytest.fixture()
def filled_playlists_cache(
    filled_cache_playlists_data: Dict[PlaylistID, Playlist]
) -> InMemoryPlaylistCache:
    return InMemoryPlaylistCache(filled_cache_playlists_data)


@pytest.fixture()
def playlist_in_memory_repo(
    playlists: Dict[PlaylistID, Playlist]
) -> InMemoryPlaylistRepository:
    return InMemoryPlaylistRepository(playlists)


@pytest.fixture()
def filled_playlists_in_memory_repo(
    filled_playlists: Dict[PlaylistID, Playlist]
) -> InMemoryPlaylistRepository:
    return InMemoryPlaylistRepository(filled_playlists)


@pytest.fixture()
def playlist_in_memory_reader(
    playlists: Dict[PlaylistID, Playlist]
) -> InMemoryPlaylistReader:
    return InMemoryPlaylistReader(playlists)


@pytest.fixture()
def filled_playlists_in_memory_reader(
    filled_playlists: Dict[PlaylistID, Playlist]
) -> InMemoryPlaylistReader:
    return InMemoryPlaylistReader(filled_playlists)
