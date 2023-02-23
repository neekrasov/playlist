import uuid
from typing import Dict

from playlist.domain.entities import Playlist, PlaylistID
from playlist.application.protocols.playlist_repo import PlaylistRepository
from playlist.application.protocols.playlist_reader import PlaylistReader


class InMemoryPlaylistRepositoryImpl(PlaylistRepository):
    def __init__(self, playlists: Dict[PlaylistID, Playlist]) -> None:
        self._playlists = playlists

    async def create_playlist(self, title: str) -> PlaylistID:
        playlist_id = PlaylistID(uuid.uuid4())
        playlist = Playlist(title, playlist_id)
        self._playlists[playlist_id] = playlist
        return playlist_id

    async def delete_playlist(self, playlist_id: PlaylistID) -> None:
        del self._playlists[playlist_id]


class InMemoryPlaylistReaderImpl(PlaylistReader):
    def __init__(self, playlists: Dict[PlaylistID, Playlist]) -> None:
        self._playlists = playlists

    async def get_playlist(self, playlist_id: PlaylistID) -> Playlist:
        return self._playlists[playlist_id]
