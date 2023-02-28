from dataclasses import dataclass

from common import Handler, UnitOfWork
from playlist.application.protocols.playlist_cache import PlaylistCache
from playlist.application.protocols.playlist_repo import PlaylistRepository
from playlist.domain.entities import Song, SongID


@dataclass
class CreateSongCommand:
    song: Song


class CreateSongHandler(Handler[CreateSongCommand, SongID]):
    def __init__(
        self,
        playlist_repo: PlaylistRepository,
        playlist_cache: PlaylistCache,
        uow: UnitOfWork,
    ):
        self._playlist_repo = playlist_repo
        self._playlist_cache = playlist_cache
        self._uow = uow

    async def execute(self, command: CreateSongCommand) -> SongID:
        async with self._uow.pipeline:
            song = command.song
            song_id = await self._playlist_repo.add_song(command.song)
            song.id = song_id

            from_cache = self._playlist_cache.get_playlist(song.playlist_id)  # type: ignore # noqa: E501
            if from_cache:
                from_cache.add_song(command.song)

            await self._uow.commit()
            return song_id
