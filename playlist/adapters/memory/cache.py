import asyncio
from typing import Dict, Optional

from playlist.application.protocols.playlist_cache import PlaylistCache
from playlist.domain.entities import Playlist, PlaylistID
from playlist.domain.exceptions import PlaylistException
from playlist.config import Settings


class InMemoryPlaylistCache(PlaylistCache):
    def __init__(
        self,
        cache_playlists: Dict[PlaylistID, Playlist],
        settings: Settings,
    ) -> None:
        self._cache_playlists = cache_playlists
        self._check_period = settings.cache_check_period

    def get_playlist(self, playlist_id: PlaylistID) -> Optional[Playlist]:
        return self._cache_playlists.get(playlist_id)

    def add_playlist(self, playlist: Playlist) -> None:
        if self._cache_playlists.get(playlist.id):  # type: ignore
            raise PlaylistException("Playlist already exists")
        self._cache_playlists[playlist.id] = playlist  # type: ignore

    def delete_playlist(self, playlist_id: PlaylistID) -> None:
        del self._cache_playlists[playlist_id]

    async def check(self, playlist: Playlist) -> None:
        while not playlist.is_stopped:
            await asyncio.sleep(self._check_period)

        del self._cache_playlists[playlist.id]  # type: ignore
