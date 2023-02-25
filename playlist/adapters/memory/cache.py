import asyncio
from typing import Dict, Optional

from playlist.application.protocols.playlist_cache import PlaylistCache
from playlist.domain.entities import Playlist, PlaylistID


class InMemoryPlaylistCache(PlaylistCache):
    def __init__(
        self,
        cache_playlists: Dict[PlaylistID, Playlist],
        check_period: int = 1,
    ) -> None:
        self._cache_playlists = cache_playlists
        self._check_period = check_period

    def get_playlist(self, playlist_id: PlaylistID) -> Optional[Playlist]:
        return self._cache_playlists.get(playlist_id)

    def add_playlist(self, playlist: Playlist) -> None:
        self._cache_playlists[playlist.id] = playlist  # type: ignore

    def delete_playlist(self, playlist_id: PlaylistID) -> None:
        del self._cache_playlists[playlist_id]

    async def check(self, playlist: Playlist) -> None:
        while not playlist.is_stopped:
            await asyncio.sleep(self._check_period)

        del self._cache_playlists[playlist.id]  # type: ignore
