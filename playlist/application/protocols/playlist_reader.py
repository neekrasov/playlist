from typing import Protocol

from playlist.domain.entities import Playlist, PlaylistID


class PlaylistReader(Protocol):
    async def get_playlist(
        self, playlist_id: PlaylistID
    ) -> Playlist:
        ...
