from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.domain.entities import PlaylistID
from ..protocols.playlist_repo import PlaylistRepository


@dataclass
class CreatePlaylistCommand:
    title: str


class CreatePlaylistHandler(Handler[CreatePlaylistCommand, PlaylistID]):
    def __init__(self, playlist_repo: PlaylistRepository, uow: UnitOfWork):
        self._playlist_repo = playlist_repo
        self._uow = uow

    async def execute(self, command: CreatePlaylistCommand) -> PlaylistID:
        async with self._uow.pipeline:
            playlist_id = await self._playlist_repo.create_playlist(
                command.title
            )
            await self._uow.commit()
            return playlist_id
