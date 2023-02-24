import pytest
import uuid
import asyncio
from playlist.domain.exceptions import (
    PlaylistNotFoundException,
    PlayListException,
    SongNotFoundException,
)
from playlist.domain.entities import PlaylistID, Song, Playlist, SongID
from playlist.application.handlers.create_playlist import (
    CreatePlaylistHandler,
    CreatePlaylistCommand,
)
from playlist.application.handlers.delete_playlist import (
    DeletePlaylistHandler,
    DeletePlaylistCommand,
)
from playlist.application.handlers.create_song import (
    CreateSongHandler,
    CreateSongCommand,
)
from playlist.application.handlers.delete_song import (
    DeleteSongHandler,
    DeleteSongCommand,
)


class TestCreatePlaylisthandler:
    @pytest.mark.asyncio
    async def test_create_playlist_handler(
        self, playlist_in_memory_repo, playlists, fake_uow
    ):
        playlist_handler = CreatePlaylistHandler(
            playlist_in_memory_repo, fake_uow
        )
        id_ = await playlist_handler.execute(
            CreatePlaylistCommand("test_playlist")
        )
        assert id_ in playlists


class TestDeletePlaylisthandler:
    @pytest.mark.asyncio
    async def test_delete_playlist_handler(
        self,
        filled_playlists_in_memory_repo,
        filled_playlists,
        playlists_cache,
        fake_uow,
    ):
        test_playlist = list(filled_playlists)[0]
        playlist_handler = DeletePlaylistHandler(
            filled_playlists_in_memory_repo, playlists_cache, fake_uow
        )
        await playlist_handler.execute(DeletePlaylistCommand(test_playlist))
        assert test_playlist not in filled_playlists

    @pytest.mark.asyncio
    async def test_delete_playlist_if_not_exists(
        self,
        playlist_in_memory_repo,
        playlists_cache,
        fake_uow,
    ):
        with pytest.raises(PlaylistNotFoundException):
            await DeletePlaylistHandler(
                playlist_in_memory_repo, playlists_cache, fake_uow
            ).execute(DeletePlaylistCommand(PlaylistID(uuid.uuid4())))

    @pytest.mark.asyncio
    async def test_delete_playing_playlist(
        self,
        playlist_in_memory_repo,
        filled_playlists_cache,
        filled_cache_playlists_data,
        fake_uow,
    ):
        cached_playlist = list(filled_cache_playlists_data.items())[0][1]
        cached_playlist.add_song(Song("test", 100))
        handler = DeletePlaylistHandler(
            playlist_in_memory_repo, filled_playlists_cache, fake_uow
        )

        async def delete():
            await asyncio.sleep(1)
            await handler.execute(DeletePlaylistCommand(cached_playlist.id))

        with pytest.raises(PlayListException):
            await asyncio.gather(cached_playlist.play(), delete())


class TestCreateSongHandler:
    @pytest.mark.asyncio
    async def test_create_song_handler(
        self,
        filled_playlists,
        filled_playlists_in_memory_repo,
        filled_cache_playlists_data,
        filled_playlists_cache,
        fake_uow,
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]

        old_size = playlist.size
        playlist_handler = CreateSongHandler(
            filled_playlists_in_memory_repo,
            filled_playlists_cache,
            fake_uow,
        )
        await playlist_handler.execute(
            CreateSongCommand(playlist.id, Song("title", 100))
        )

        assert playlist.size == old_size + 1
        assert playlist_from_cache.size == old_size + 1

    @pytest.mark.asyncio
    async def test_create_song_if_playlist_not_exists(
        self,
        playlist_in_memory_repo,
        playlists_cache,
        fake_uow,
    ):
        with pytest.raises(PlaylistNotFoundException):
            await CreateSongHandler(
                playlist_in_memory_repo, playlists_cache, fake_uow
            ).execute(
                CreateSongCommand(PlaylistID(uuid.uuid4()), Song("title", 100))
            )

    @pytest.mark.asyncio
    async def test_create_song_in_playing_playlist(
        self,
        filled_cache_playlists_data,
        filled_playlists,
        filled_playlists_in_memory_repo,
        filled_playlists_cache,
        fake_uow,
    ):
        cached_playlist = list(filled_cache_playlists_data.items())[0][1]
        memory_playlist = list(filled_playlists.items())[0][1]

        old_size = cached_playlist.size

        async def create():
            await asyncio.sleep(1)
            await CreateSongHandler(
                filled_playlists_in_memory_repo,
                filled_playlists_cache,
                fake_uow,
            ).execute(
                CreateSongCommand(cached_playlist.id, Song("title", 100))
            )

        async def asserting():
            await asyncio.sleep(2)
            assert cached_playlist.size == old_size + 1
            assert memory_playlist.size == old_size + 1

            cached_playlist.pause()

        await asyncio.gather(cached_playlist.play(), create(), asserting())


class TestDeleteSongHandler:
    @pytest.mark.asyncio
    async def test_delete_song_handler(
        self,
        filled_playlists,
        filled_playlists_in_memory_repo,
        filled_cache_playlists_data,
        filled_playlists_cache,
        songs_id,
        fake_uow,
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]
        delete_song_id: SongID = songs_id[0]
        old_size = playlist.size

        assert playlist.get_song(delete_song_id) is not None
        assert playlist_from_cache.get_song(delete_song_id) is not None

        handler = DeleteSongHandler(
            filled_playlists_in_memory_repo,
            filled_playlists_cache,
            fake_uow,
        )
        await handler.execute(DeleteSongCommand(playlist.id, delete_song_id))

        assert playlist.size == old_size - 1
        assert playlist_from_cache.size == old_size - 1
        assert playlist.get_song(delete_song_id) is None
        assert playlist_from_cache.get_song(delete_song_id) is None

    @pytest.mark.asyncio
    async def test_delete_song_if_not_exists(
        self,
        filled_playlists,
        filled_playlists_in_memory_repo,
        filled_cache_playlists_data,
        filled_playlists_cache,
        songs_id,
        fake_uow,
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]
        with pytest.raises(SongNotFoundException):
            await DeleteSongHandler(
                filled_playlists_in_memory_repo,
                filled_playlists_cache,
                fake_uow,
            ).execute(DeleteSongCommand(playlist.id, SongID(uuid.uuid4())))
