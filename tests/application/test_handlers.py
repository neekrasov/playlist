import pytest
from playlist.application.handlers.create_playlist import (
    CreatePlaylistHandler,
    CreatePlaylistCommand,
)
from playlist.application.handlers.delete_playlist import (
    DeletePlaylistHandler,
    DeletePlaylistCommand,
)


@pytest.mark.asyncio
async def test_create_playlist_handler(playlist_in_memory_repo, playlists):
    playlist_handler = CreatePlaylistHandler(playlist_in_memory_repo)
    id_ = await playlist_handler.execute(
        CreatePlaylistCommand("test_playlist")
    )
    assert id_ in playlists


@pytest.mark.asyncio
async def test_delete_playlist_handler(
    filled_playlists_in_memory_repo, filled_playlists
):
    test_playlist = list(filled_playlists)[0]
    playlist_handler = DeletePlaylistHandler(filled_playlists_in_memory_repo)
    await playlist_handler.execute(DeletePlaylistCommand(test_playlist))
    assert test_playlist not in filled_playlists
