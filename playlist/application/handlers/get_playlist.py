from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.application.protocols import PlaylistReader, PlaylistCache
from playlist.domain.entities import PlaylistID, PlaylistState


@dataclass
class GetPlaylistCommand:
    playlist_id: PlaylistID


@dataclass
class GetPlaylistDTO:
    id: PlaylistID
    title: str
    status: PlaylistState


class GetPlaylistHandler(Handler[GetPlaylistCommand, GetPlaylistDTO]):
    def __init__(
        self,
        playlist_reader: PlaylistReader,
        playlist_cache: PlaylistCache,
        uow: UnitOfWork,
    ):
        self._playlist_reader = playlist_reader
        self._playlist_cache = playlist_cache
        self._uow = uow

    async def execute(self, command: GetPlaylistCommand) -> GetPlaylistDTO:
        async with self._uow.pipeline:
            playlist = await self._playlist_reader.get_playlist_by_id(
                command.playlist_id
            )
            from_cache = self._playlist_cache.get_playlist(command.playlist_id)
            if from_cache and not from_cache.is_stopped:
                return GetPlaylistDTO(
                    command.playlist_id, playlist.title, from_cache.state
                )

            return GetPlaylistDTO(
                command.playlist_id, playlist.title, PlaylistState.STOPPED
            )
