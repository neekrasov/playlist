import pytest
import uuid
from typing import Dict
from playlist.domain.entities import Playlist, PlaylistID
from playlist.adapters.memory.playlist_repo_impl import (
    InMemoryPlaylistRepositoryImpl,
)


@pytest.fixture(scope="session")
def playlists() -> Dict[PlaylistID, Playlist]:
    return {}


@pytest.fixture(scope="session")
def filled_playlists() -> Dict[PlaylistID, Playlist]:
    uuid1 = uuid.uuid4()
    uuid2 = uuid.uuid4()
    return {
        PlaylistID(uuid1): Playlist(
            id=PlaylistID(uuid1),
            title="Playlist 1",
        ),
        PlaylistID(uuid2): Playlist(
            id=PlaylistID(uuid2),
            title="Playlist 2",
        ),
    }


@pytest.fixture()
def playlist_in_memory_repo(playlists: Dict[PlaylistID, Playlist]):
    return InMemoryPlaylistRepositoryImpl(playlists)


@pytest.fixture()
def filled_playlists_in_memory_repo(
    filled_playlists: Dict[PlaylistID, Playlist]
):
    return InMemoryPlaylistRepositoryImpl(filled_playlists)
