from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.application.protocols import PlaylistReader
from playlist.domain.entities import PlaylistID, SongID
from playlist.domain.exceptions import SongNotFoundException


@dataclass
class GetSongCommand:
    playlist_id: PlaylistID
    song_id: SongID


@dataclass
class GetSongDTO:
    id: SongID
    title: str
    duration: float


class GetSongHandler(Handler[GetSongCommand, GetSongDTO]):
    def __init__(
        self,
        playlist_reader: PlaylistReader,
        uow: UnitOfWork,
    ):
        self._playlist_reader = playlist_reader
        self._uow = uow

    async def execute(self, command: GetSongCommand) -> GetSongDTO:
        async with self._uow.pipeline:
            playlist = await self._playlist_reader.get_playlist_by_id(
                command.playlist_id
            )
            song = playlist.get_song(command.song_id)
            if song is None:
                raise SongNotFoundException(command.song_id)
            return GetSongDTO(
                id=song.id,  # type: ignore
                title=song.title,
                duration=song.duration,
            )
