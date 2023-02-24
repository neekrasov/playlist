from dataclasses import dataclass

from common import Handler
from playlist.domain.entities import PlaylistID
from playlist.domain.exceptions import PlaylistNotFoundException
from playlist.application.protocols import PlaylistCache


@dataclass
class PauseSongCommand:
    playlist_id: PlaylistID


class PauseSongHandler(Handler[PauseSongCommand, None]):
    def __init__(self, playlist_cache: PlaylistCache):
        self._playlist_cache = playlist_cache

    async def execute(self, command: PauseSongCommand) -> None:
        from_cache = self._playlist_cache.get_playlist(command.playlist_id)

        if not from_cache:
            raise PlaylistNotFoundException(command.playlist_id)

        from_cache.pause()
