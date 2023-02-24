from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.domain.entities import SongID, PlaylistID
from playlist.application.protocols.playlist_cache import PlaylistCache
from playlist.application.protocols.playlist_repo import PlaylistRepository


@dataclass
class DeleteSongCommand:
    playlist_id: PlaylistID
    song_id: SongID


class DeleteSongHandler(Handler[DeleteSongCommand, None]):
    def __init__(
        self,
        playlist_repo: PlaylistRepository,
        playlist_cache: PlaylistCache,
        uow: UnitOfWork,
    ):
        self._playlist_repo = playlist_repo
        self._playlist_cache = playlist_cache
        self._uow = uow

    async def execute(self, command: DeleteSongCommand) -> None:
        async with self._uow.pipeline:
            from_cache = self._playlist_cache.get_playlist(command.playlist_id)

            if from_cache:
                from_cache.remove_song(command.song_id)

            await self._playlist_repo.delete_song(
                command.playlist_id, command.song_id
            )

            await self._uow.commit()
