from sqlalchemy.sql import delete, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from playlist.application.protocols import PlaylistRepository
from playlist.domain.entities import Playlist, Song, PlaylistID, SongID
from playlist.domain.exceptions import (
    SongNotFoundException,
)


class PlaylistRepositoryImpl(PlaylistRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_playlist(self, title: str) -> PlaylistID:
        playlist = Playlist(title)
        self._session.add(playlist)
        await self._session.flush()
        await self._session.refresh(playlist)
        return playlist.id  # type: ignore

    async def delete_playlist(self, playlist_id: PlaylistID) -> None:
        await self._session.execute(
            delete(Playlist).where(Playlist.id == playlist_id)  # type: ignore
        )

    async def add_song(self, song: Song) -> None:
        self._session.add(song)

    async def delete_song(
        self,
        playlist_id: PlaylistID,
        song_id: SongID,
    ) -> None:
        await self._get_song(song_id, playlist_id)
        await self._session.execute(
            delete(Song).where(
                and_(
                    Song.id == song_id,  # type: ignore
                    Song.playlist_id == playlist_id,  # type: ignore
                )
            )
        )

    async def update_song(
        self,
        song: Song,
    ) -> None:
        db_song = await self._get_song(
            song.id, song.playlist_id  # type: ignore
        )

        db_song.title = song.title
        db_song.duration = song.duration

    async def _get_song(
        self, song_id: SongID, playlist_id: PlaylistID
    ) -> Song:
        song_result = await self._session.execute(
            select(Song).where(
                and_(
                    Song.id == song_id,  # type: ignore
                    Song.playlist_id == playlist_id,  # type: ignore
                )
            )
        )
        song = song_result.scalar_one_or_none()
        if not song:
            raise SongNotFoundException(song_id)
        return song
