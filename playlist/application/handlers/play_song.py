from dataclasses import dataclass

from common import Handler, UnitOfWork
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
        uow: UnitOfWork,
    ):
        self._playlist_reader = playlist_reader
        self._playlist_cache = playlist_cache
        self._uow = uow

    async def execute(self, command: PlaySongCommand) -> None:
        from_cache = self._playlist_cache.get_playlist(command.playlist_id)

        if from_cache:
            await from_cache.play()
        else:
            playlist = await self._playlist_reader.get_playlist(
                command.playlist_id
            )
            self._playlist_cache.add_playlist(playlist)
            await playlist.play()
