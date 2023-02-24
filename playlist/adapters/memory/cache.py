from typing import Dict, Optional

from playlist.application.protocols.playlist_cache import PlaylistCache
from playlist.domain.entities import Playlist, PlaylistID


class InMemoryPlaylistCache(PlaylistCache):
    def __init__(self, cache_playlists: Dict[PlaylistID, Playlist]) -> None:
        self._cache_playlists = cache_playlists

    def get_playlist(self, playlist_id: PlaylistID) -> Optional[Playlist]:
        return self._cache_playlists.get(playlist_id)

    def add_playlist(self, playlist: Playlist) -> None:
        self._cache_playlists[playlist.id] = playlist  # type: ignore

    def delete_playlist(self, playlist_id: PlaylistID) -> None:
        del self._cache_playlists[playlist_id]
