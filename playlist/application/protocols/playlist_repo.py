from typing import Protocol

from playlist.domain.entities import PlaylistID, Song, SongID


class PlaylistRepository(Protocol):
    async def create_playlist(self, title: str) -> PlaylistID:
        ...

    async def delete_playlist(self, playlist_id: PlaylistID) -> None:
        ...

    async def add_song(self, song: Song) -> SongID:
        ...

    async def delete_song(
        self, playlist_id: PlaylistID, song_id: SongID
    ) -> None:
        ...

    async def update_song(self, song: Song) -> None:
        ...
