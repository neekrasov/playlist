import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from playlist.domain.entities import Playlist, Song
from playlist.domain.exceptions import SongNotFoundException
from playlist.adapters.sqlalchemy.repo import PlaylistRepositoryImpl
from playlist.adapters.sqlalchemy.reader import PlaylistReaderImpl


class TestSqlachemyRepository:
    @pytest.mark.asyncio
    async def test_create_playlist(
        self,
        playlists_repository: PlaylistRepositoryImpl,
        session: AsyncSession,
    ):
        playlist_id = await playlists_repository.create_playlist("test")
        playlist = await session.get(Playlist, playlist_id)

        assert playlist_id is not None
        assert playlist is not None
        assert playlist.id == playlist_id

    @pytest.mark.asyncio
    async def test_delete_playlist(
        self,
        playlists_repository: PlaylistRepositoryImpl,
        session: AsyncSession,
        playlists_id,
        fill_db_data,
    ):
        playlist_before = await session.get(Playlist, playlists_id[0])
        await playlists_repository.delete_playlist(playlists_id[0])
        playlist = await session.get(Playlist, playlists_id[0])

        await session.rollback()
        assert playlist_before is not None
        assert playlist is None

    @pytest.mark.asyncio
    async def test_add_song(
        self,
        playlists_repository: PlaylistRepositoryImpl,
        playlists_reader: PlaylistReaderImpl,
        session: AsyncSession,
        playlists_id,
        fill_db_data,
    ):
        playlist_id = playlists_id[1]
        old_playlist = await playlists_reader.get_playlist_by_id(playlist_id)
        await playlists_repository.add_song(
            Song(title="test", duration=100, playlist_id=playlist_id, id=None)
        )
        await session.commit()
        new_playlist = await playlists_reader.get_playlist_by_id(playlist_id)
        assert old_playlist is not None
        assert new_playlist is not None
        assert new_playlist.size == old_playlist.size + 1

    @pytest.mark.asyncio
    async def test_delete_song(
        self,
        playlists_repository: PlaylistRepositoryImpl,
        session: AsyncSession,
        playlists_id,
        songs_id,
        fill_db_data,
    ):
        song_id = songs_id[3]
        playlist = await session.get(Playlist, playlists_id[1])
        song = await session.get(Song, song_id)

        assert song is not None

        await playlists_repository.delete_song(playlist.id, song.id)  # type: ignore # noqa
        await session.commit()

        song = await session.get(Song, song_id)
        await session.rollback()
        assert song is None

    @pytest.mark.asyncio
    async def test_delete_song_not_in_playlist(
        self,
        playlists_repository: PlaylistRepositoryImpl,
        session: AsyncSession,
        playlists_id,
        songs_id,
        fill_db_data,
    ):
        song_id = songs_id[1]
        playlist = await session.get(Playlist, playlists_id[1])
        song = await session.get(Song, song_id)

        with pytest.raises(SongNotFoundException):
            await playlists_repository.delete_song(playlist.id, song.id)  # type: ignore # noqa

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_song(
        self,
        playlists_repository: PlaylistRepositoryImpl,
        playlists_reader: PlaylistReaderImpl,
        session: AsyncSession,
        playlists_id,
        songs_id,
        fill_db_data,
    ):
        song_id = songs_id[0]
        playlist = await session.get(Playlist, playlists_id[0])
        before_song = await session.get(Song, song_id)

        before_title = before_song.title  # type: ignore
        before_duration = before_song.duration  # type: ignore

        assert before_song is not None

        await playlists_repository.update_song(
            Song(
                title="test",
                duration=110,
                playlist_id=playlist.id,  # type: ignore
                id=song_id,
            )
        )
        await session.commit()

        song = await session.get(Song, song_id)
        assert before_song.id == song.id  # type: ignore
        assert before_song.title != before_title
        assert before_song.duration != int(before_duration)
