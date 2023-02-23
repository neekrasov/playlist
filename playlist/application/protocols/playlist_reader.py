from typing import Protocol, Optional

from playlist.domain.entities import Playlist, PlaylistID


class PlaylistReader(Protocol):
    async def get_playlist(
        self, playlist_id: PlaylistID
    ) -> Optional[Playlist]:
        ...
