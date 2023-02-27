import pytest

from playlist.adapters.grpc.generated.playlist_pb2_grpc import PlayListStub
from playlist.adapters.grpc.generated.playlist_pb2 import (
    CreatePlaylistRequest,
    CreatePlaylistResponse,
    DeletePlaylistRequest,
    DeletePlaylistResponse,
    GetPlaylistRequest,
    GetPlaylistResponse,
)


class TestPlaylistRpc:
    @pytest.mark.asyncio
    async def test_create_playlist(
        self,
        playlist_stub: PlayListStub,
    ):
        request = CreatePlaylistRequest(title="test")
        response = await playlist_stub.CreatePlaylist(request)
        assert isinstance(response, CreatePlaylistResponse)

    @pytest.mark.asyncio
    async def test_delete_playlist(
        self, playlist_stub: PlayListStub, fill_db_data, playlists_id,
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
