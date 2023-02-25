from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.domain.entities import PlaylistID
from playlist.domain.exceptions import PlaylistException
from ..protocols.playlist_repo import PlaylistRepository
from ..protocols.playlist_cache import PlaylistCache


@dataclass
class DeletePlaylistCommand:
    playlist_id: PlaylistID


class DeletePlaylistHandler(Handler[DeletePlaylistCommand, None]):
    def __init__(
        self,
        playlist_repo: PlaylistRepository,
        cache: PlaylistCache,
        uow: UnitOfWork,
    ):
        self._playlist_repo = playlist_repo
        self._cache = cache
        self._uow = uow

    async def execute(self, command: DeletePlaylistCommand) -> None:
        async with self._uow.pipeline:
            from_cache = self._cache.get_playlist(command.playlist_id)
            if from_cache:
                if from_cache.is_playing:
                    raise PlaylistException(
                        "Cannot delete a playlist that is playing"
                    )
                self._cache.delete_playlist(command.playlist_id)

            await self._playlist_repo.delete_playlist(command.playlist_id)
            await self._uow.commit()
