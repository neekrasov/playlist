import asyncio
import pytest
import uuid
from sqlalchemy.sql import delete
from sqlalchemy.ext.asyncio import AsyncSession

from playlist.domain.entities import Playlist
from playlist.adapters.grpc.generated.song_pb2_grpc import SongStub
from playlist.adapters.grpc.generated.playlist_pb2_grpc import PlayListStub
from playlist.adapters.grpc.generated.control_pb2_grpc import (
    PlaylistControlStub,
)
from playlist.adapters.grpc.generated.playlist_pb2 import (
    CreatePlaylistRequest,
    CreatePlaylistResponse,
    DeletePlaylistRequest,
    DeletePlaylistResponse,
    GetPlaylistRequest,
    GetPlaylistResponse,
)
from playlist.adapters.grpc.generated.song_pb2 import (
    SongMessage,
    CreateSongRequest,
    CreateSongResponse,
    DeleteSongRequest,
    DeleteSongResponse,
    GetSongRequest,
    GetSongResponse,
    UpdateSongRequest,
    UpdateSongResponse,
)
from playlist.adapters.grpc.generated.control_pb2 import (
    PlaySongRequest,
    PlaySongResponse,
    PauseSongRequest,
    PauseSongResponse,
    NextSongRequest,
    NextSongResponse,
    PrevSongRequest,
    PrevSongResponse,
)


class TestPlaylistRpc:
    @pytest.mark.asyncio
    async def test_create_playlist(
        self,
        playlist_stub: PlayListStub,
        session: AsyncSession,
    ):
        request = CreatePlaylistRequest(title="test")
        response = await playlist_stub.CreatePlaylist(request)

        await session.execute(
            delete(Playlist).where(Playlist.id == uuid.UUID(bytes=response.id))  # type: ignore # noqa
        )
        await session.commit()

        assert isinstance(response, CreatePlaylistResponse)

    @pytest.mark.asyncio
    async def test_delete_playlist(
        self,
        playlist_stub: PlayListStub,
        fill_db_data,
        playlists_id,
    ):
        request = DeletePlaylistRequest(playlist_id=playlists_id[0].bytes)
        response = await playlist_stub.DeletePlaylist(request)
        assert isinstance(response, DeletePlaylistResponse)

    @pytest.mark.asyncio
    async def test_get_playlist(
        self, playlist_stub: PlayListStub, fill_db_data, playlists_id
    ):
        request = GetPlaylistRequest(playlist_id=playlists_id[1].bytes)
        response = await playlist_stub.GetPlaylist(request)
        assert isinstance(response, GetPlaylistResponse)


class TestSongRpc:
    @pytest.mark.asyncio
    async def test_create_song(
        self,
        song_stub: SongStub,
        fill_db_data,
        playlists_id,
    ):
        response = await song_stub.CreateSong(
            CreateSongRequest(
                playlist_id=playlists_id[0].bytes,
                song=SongMessage(title="test", duration=100),
            )
        )
        assert isinstance(response, CreateSongResponse)

    @pytest.mark.asyncio
    async def test_delete_song(
        self,
        song_stub: SongStub,
        fill_db_data,
        playlists_id,
        songs_id,
        session,
    ):
        response = await song_stub.DeleteSong(
            DeleteSongRequest(
                playlist_id=playlists_id[0].bytes, song_id=songs_id[0].bytes
            )
        )

        assert isinstance(response, DeleteSongResponse)

    @pytest.mark.asyncio
    async def test_get_song(
        self,
        song_stub: SongStub,
        fill_db_data,
        playlists_id,
        db_songs,
    ):
        response = await song_stub.GetSong(
            GetSongRequest(
                playlist_id=playlists_id[0].bytes, song_id=db_songs[1].id.bytes
            )
        )
        assert isinstance(response, GetSongResponse)
        assert response.song.title == db_songs[1].title

    @pytest.mark.asyncio
    async def test_update_song(
        self,
        song_stub: SongStub,
        session: AsyncSession,
        db_songs,
        fill_db_data,
        playlists_id,
    ):
        response = await song_stub.UpdateSong(
            UpdateSongRequest(
                playlist_id=playlists_id[0].bytes,
                song_id=db_songs[1].id.bytes,
                song=SongMessage(title="test", duration=120),
            )
        )
        assert isinstance(response, UpdateSongResponse)


class TestControlRpc:
    @pytest.mark.asyncio
    async def test_play_song(
        self,
        control_stub: PlaylistControlStub,
        fill_db_data,
        playlists_id,
    ):
        response = await control_stub.PlaySong(
            PlaySongRequest(playlist_id=playlists_id[0].bytes)
        )
        assert isinstance(response, PlaySongResponse)

    @pytest.mark.asyncio
    async def test_pause_song(
        self,
        control_stub: PlaylistControlStub,
        fill_db_data,
        db_playlists,
    ):
        async def pause():
            await asyncio.sleep(1)
            response = await control_stub.PauseSong(
                PauseSongRequest(playlist_id=db_playlists[1].id.bytes)
            )
            assert isinstance(response, PauseSongResponse)

        await asyncio.gather(
            control_stub.PlaySong(
                PlaySongRequest(playlist_id=db_playlists[1].id.bytes)
            ),
            pause(),
        )

    @pytest.mark.asyncio
    async def test_next_song(
        self,
        control_stub: PlaylistControlStub,
        fill_db_data,
        db_playlists,
    ):
        async def next():
            await asyncio.sleep(1)
            response = await control_stub.NextSong(
                NextSongRequest(playlist_id=db_playlists[1].id.bytes)
            )
            await control_stub.PauseSong(
                PauseSongRequest(playlist_id=db_playlists[1].id.bytes)
            )
            assert isinstance(response, NextSongResponse)

        await asyncio.gather(
            control_stub.PlaySong(
                PlaySongRequest(playlist_id=db_playlists[1].id.bytes)
            ),
            next(),
        )

    @pytest.mark.asyncio
    async def test_prev_song(
        self,
        control_stub: PlaylistControlStub,
        fill_db_data,
        db_playlists,
    ):
        async def prev():
            await asyncio.sleep(2)
            response = await control_stub.PrevSong(
                PrevSongRequest(playlist_id=db_playlists[0].id.bytes)
            )
            await control_stub.PauseSong(
                PauseSongRequest(playlist_id=db_playlists[0].id.bytes)
            )
            assert isinstance(response, PrevSongResponse)

        await asyncio.gather(
            control_stub.PlaySong(
                PlaySongRequest(playlist_id=db_playlists[0].id.bytes)
            ),
            prev(),
        )
