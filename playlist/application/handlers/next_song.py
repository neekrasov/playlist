from dataclasses import dataclass

from common import Handler
from playlist.domain.entities import PlaylistID
from playlist.domain.exceptions import PlaylistNotFoundException
from playlist.application.protocols import PlaylistCache


@dataclass
class NextSongCommand:
    playlist_id: PlaylistID


class NextSongHandler(Handler[NextSongCommand, None]):
    def __init__(self, playlist_cache: PlaylistCache):
        self._playlist_cache = playlist_cache

    async def execute(self, command: NextSongCommand) -> None:
        from_cache = self._playlist_cache.get_playlist(command.playlist_id)

        if not from_cache:
            raise PlaylistNotFoundException(command.playlist_id)

        from_cache.next()
