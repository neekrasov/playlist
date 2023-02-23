from typing import Protocol

from playlist.domain.entities import PlaylistID


class PlaylistRepository(Protocol):
    async def create_playlist(self, title: str) -> PlaylistID:
        ...

    async def delete_playlist(self, playlist_id: PlaylistID) -> None:
        ...
