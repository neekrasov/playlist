import uuid
import pytest
import grpc
import asyncio

from playlist.adapters.grpc.generated.playlist_pb2_grpc import PlayListStub
from playlist.adapters.grpc.generated.playlist_pb2 import (
    DeletePlaylistRequest,
)
from playlist.adapters.grpc.generated.control_pb2_grpc import (
    PlaylistControlStub,
)
from playlist.adapters.grpc.generated.control_pb2 import (
    PlaySongRequest,
    PauseSongRequest,
    NextSongRequest,
)


class TestRpcErrors:
    @pytest.mark.asyncio
    async def test_delete_playlist_not_found(
        self, playlist_stub: PlayListStub
    ):
        uuid_ = uuid.uuid4()
        request = DeletePlaylistRequest(playlist_id=uuid_.bytes)
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await playlist_stub.DeletePlaylist(request)

        assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    @pytest.mark.asyncio
    async def test_pause_song_not_found(
        self, control_stub: PlaylistControlStub
    ):
        uuid_ = uuid.uuid4()
        request = PauseSongRequest(playlist_id=uuid_.bytes)
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await control_stub.PauseSong(request)

        assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    @pytest.mark.asyncio
    async def test_play_song_not_found(
        self, control_stub: PlaylistControlStub
    ):
        uuid_ = uuid.uuid4()
        request = PlaySongRequest(playlist_id=uuid_.bytes)
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await control_stub.PlaySong(request)

        assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    @pytest.mark.asyncio
    async def test_next_not_playing(
        self, control_stub: PlaylistControlStub, playlists_id, fill_db_data
    ):
        request = NextSongRequest(playlist_id=playlists_id[0].bytes)
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await control_stub.NextSong(request)

        assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    @pytest.mark.asyncio
    async def test_double_play(
        self, control_stub: PlaylistControlStub, playlists_id, fill_db_data
    ):
        request = PlaySongRequest(playlist_id=playlists_id[1].bytes)
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await asyncio.gather(
                control_stub.PlaySong(request), control_stub.PlaySong(request)
            )

        assert exc_info.value.code() == grpc.StatusCode.ABORTED
