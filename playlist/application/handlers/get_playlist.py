from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.application.protocols import PlaylistReader
from playlist.domain.entities import PlaylistID


@dataclass
class GetPlaylistCommand:
    playlist_id: PlaylistID


@dataclass
class GetPlaylistDTO:
    id: PlaylistID
    title: str


class GetPlaylistHandler(Handler[GetPlaylistCommand, GetPlaylistDTO]):
    def __init__(
        self,
        playlist_reader: PlaylistReader,
        uow: UnitOfWork,
    ):
        self._playlist_reader = playlist_reader
        self._uow = uow

    async def execute(self, command: GetPlaylistCommand) -> GetPlaylistDTO:
        async with self._uow.pipeline:
            playlist = await self._playlist_reader.get_playlist_by_id(
                command.playlist_id
            )
            return GetPlaylistDTO(playlist.id, playlist.title)  # type: ignore
