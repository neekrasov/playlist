from sqlalchemy.sql import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from playlist.domain.entities import PlaylistID, Playlist, Song
from playlist.domain.exceptions import PlaylistNotFoundException
from playlist.application.protocols import PlaylistReader


class PlaylistReaderImpl(PlaylistReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_playlist_by_id(self, playlist_id: PlaylistID) -> Playlist:
        stmt_playlist = select(Playlist).where(Playlist.id == playlist_id)  # type: ignore # noqa
        result_playlist = await self._session.execute(stmt_playlist)
        playlist: Playlist = result_playlist.scalar_one_or_none()  # type: ignore # noqa
        if not playlist:
            raise PlaylistNotFoundException(playlist_id)

        playlist = Playlist(id=playlist.id, title=playlist.title)

        stmt_song = select(Song).where(Song.playlist_id == playlist_id).order_by(asc(Song.timestamp))  # type: ignore # noqa
        result_song = await self._session.execute(stmt_song)
        songs = result_song.scalars().all()
        for song in songs:
            playlist.add_song(song)

        return playlist
