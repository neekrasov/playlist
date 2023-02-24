from typing import Protocol, Optional

from playlist.domain.entities import Playlist, PlaylistID


class PlaylistCache(Protocol):
    def get_playlist(self, playlist_id: PlaylistID) -> Optional[Playlist]:
        ...

    def add_playlist(self, playlist: Playlist) -> None:
        ...

    def delete_playlist(self, playlist_id: PlaylistID) -> None:
        ...
