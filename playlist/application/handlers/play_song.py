import asyncio
from dataclasses import dataclass

from common import Handler
from playlist.domain.entities import PlaylistID
from playlist.application.protocols import PlaylistReader, PlaylistCache


@dataclass
class PlaySongCommand:
    playlist_id: PlaylistID


class PlaySongHandler(Handler[PlaySongCommand, None]):
    def __init__(
        self,
        playlist_reader: PlaylistReader,
        playlist_cache: PlaylistCache,
    ):
        self._playlist_reader = playlist_reader
        self._playlist_cache = playlist_cache

    async def execute(self, command: PlaySongCommand) -> None:
        from_cache = self._playlist_cache.get_playlist(command.playlist_id)

        if from_cache:
            await from_cache.play()
        else:
            playlist = await self._playlist_reader.get_playlist_by_id(
                command.playlist_id
            )
            self._playlist_cache.add_playlist(playlist)
            await asyncio.gather(
                playlist.play(), self._playlist_cache.check(playlist)
            )
