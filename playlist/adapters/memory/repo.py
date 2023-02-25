import uuid
from typing import Dict

from playlist.domain.entities import Playlist, PlaylistID, SongID, Song
from playlist.application.protocols.playlist_repo import PlaylistRepository
from playlist.application.protocols.playlist_reader import PlaylistReader
from playlist.domain.exceptions import (
    PlaylistNotFoundException,
)


class InMemoryPlaylistRepository(PlaylistRepository):
    def __init__(self, playlists: Dict[PlaylistID, Playlist]) -> None:
        self._playlists = playlists

    def _get(self, playlist_id: PlaylistID) -> Playlist:
        playlist = self._playlists.get(playlist_id)
        if not playlist:
            raise PlaylistNotFoundException(playlist_id)
        return playlist

    async def create_playlist(self, title: str) -> PlaylistID:
        playlist_id = PlaylistID(uuid.uuid4())
        playlist = Playlist(title, playlist_id)
        self._playlists[playlist_id] = playlist
        return playlist_id

    async def delete_playlist(self, playlist_id: PlaylistID) -> None:
        self._get(playlist_id)
        del self._playlists[playlist_id]

    async def delete_song(
        self, playlist_id: PlaylistID, song_id: SongID
    ) -> None:
        playlist = self._get(playlist_id)
        playlist.remove_song(song_id)

    async def add_song(self, song: Song) -> None:
        playlist = self._get(song.playlist_id)  # type: ignore
        playlist.add_song(song)

    async def update_song(self, song: Song):
        playlist = self._get(song.playlist_id)  # type: ignore
        playlist.update_song(song)


class InMemoryPlaylistReaderImpl(PlaylistReader):
    def __init__(self, playlists: Dict[PlaylistID, Playlist]) -> None:
        self._playlists = playlists

    async def get_playlist(self, playlist_id: PlaylistID) -> Playlist:
        playlist = self._playlists.get(playlist_id)
        if not playlist:
            raise PlaylistNotFoundException(playlist_id)
        return playlist
