from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.application.protocols.playlist_cache import PlaylistCache
from playlist.application.protocols.playlist_repo import PlaylistRepository
from playlist.domain.entities import Song


@dataclass
class UpdateSongCommand:
    song: Song


class UpdateSongHandler(Handler[UpdateSongCommand, None]):
    def __init__(
        self,
        playlist_repo: PlaylistRepository,
        playlist_cache: PlaylistCache,
        uow: UnitOfWork,
    ):
        self._playlist_repo = playlist_repo
        self._playlist_cache = playlist_cache
        self._uow = uow

    async def execute(self, command: UpdateSongCommand) -> None:
        async with self._uow.pipeline:
            song = command.song

            from_cache = self._playlist_cache.get_playlist(song.playlist_id)  # type: ignore # noqa: E501
            if from_cache:
                from_cache.update_song(song)
            await self._playlist_repo.update_song(song)
            await self._uow.commit()
