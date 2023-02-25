import pytest
import uuid
import asyncio

from playlist.domain.exceptions import (
    PlaylistNotFoundException,
    PlaylistException,
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
from playlist.application.handlers.play_song import (
    PlaySongHandler,
    PlaySongCommand,
)
from playlist.application.handlers.pause_song import (
    PauseSongHandler,
    PauseSongCommand,
)
from playlist.application.handlers.next_song import (
    NextSongHandler,
    NextSongCommand,
)
from playlist.application.handlers.prev_song import (
    PrevSongHandler,
    PrevSongCommand,
)
from playlist.application.handlers.get_playlist import (
    GetPlaylistCommand,
    GetPlaylistHandler,
)
from playlist.application.handlers.get_song import (
    GetSongCommand,
    GetSongHandler,
)
from playlist.application.handlers.update_song import (
    UpdateSongHandler,
    UpdateSongCommand,
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

        with pytest.raises(PlaylistException):
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

            cached_playlist.stop()

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


class TestBasePlaylistsActions:
    @pytest.mark.asyncio
    async def test_play_song_from_cache(
        self,
        playlist_in_memory_repo,
        filled_cache_playlists_data,
        filled_playlists_cache,
    ):
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]

        async def play():
            await PlaySongHandler(
                playlist_in_memory_repo,
                filled_playlists_cache,
            ).execute(PlaySongCommand(playlist_from_cache.id))

        async def check():
            await asyncio.sleep(1)

            assert playlist_from_cache.is_playing is True
            assert playlist_from_cache.current_song is not None
            assert (
                playlist_from_cache.current_song.id
                == playlist_from_cache.current_song.id
            )
            playlist_from_cache.stop()

        await asyncio.gather(play(), check())

    @pytest.mark.asyncio
    async def test_play_song_from_repo(
        self,
        filled_playlists,
        filled_playlists_in_memory_reader,
        playlists_cache,
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]

        async def play():
            await PlaySongHandler(
                filled_playlists_in_memory_reader,
                playlists_cache
            ).execute(PlaySongCommand(playlist.id))

        async def check():
            await asyncio.sleep(1)

            assert playlist.is_playing is True
            assert playlist.current_song is not None
            assert playlist.current_song.id == playlist.current_song.id
            playlist.stop()

        await asyncio.gather(play(), check())

    @pytest.mark.asyncio
    async def test_pause_song(
        self,
        filled_cache_playlists_data,
        filled_playlists_cache,
    ):
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]

        async def pause():
            await PauseSongHandler(
                filled_playlists_cache,
            ).execute(PauseSongCommand(playlist_from_cache.id))

        async def check():
            await asyncio.sleep(1)

            assert playlist_from_cache.is_playing is False

        await asyncio.gather(playlist_from_cache.play(), pause(), check())

    @pytest.mark.asyncio
    async def test_next_song(
        self,
        filled_cache_playlists_data,
        filled_playlists_cache,
    ):
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]
        old_song = playlist_from_cache.current_song

        async def next():
            await NextSongHandler(
                filled_playlists_cache,
            ).execute(NextSongCommand(playlist_from_cache.id))

        async def check():
            await asyncio.sleep(1)

            assert playlist_from_cache.is_playing is True
            assert playlist_from_cache.current_song is not None
            assert playlist_from_cache.current_song != old_song
            playlist_from_cache.stop()

        await asyncio.gather(playlist_from_cache.play(), next(), check())

    @pytest.mark.asyncio
    async def test_previous_song(
        self,
        filled_cache_playlists_data,
        filled_playlists_cache,
    ):
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]
        old_song = playlist_from_cache.current_song

        async def previous():
            await PrevSongHandler(
                filled_playlists_cache,
            ).execute(PrevSongCommand(playlist_from_cache.id))

        async def check():
            await asyncio.sleep(1)

            assert playlist_from_cache.is_playing is True
            assert playlist_from_cache.current_song is not None
            assert playlist_from_cache.current_song != old_song
            playlist_from_cache.stop()

        await asyncio.gather(playlist_from_cache.play(), previous(), check())

    @pytest.mark.asyncio
    async def test_get_playlist(
        self, filled_playlists, filled_playlists_in_memory_reader, fake_uow
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]

        playlist_from_handler = await GetPlaylistHandler(
            filled_playlists_in_memory_reader, fake_uow
        ).execute(GetPlaylistCommand(playlist.id))

        assert playlist_from_handler.id == playlist.id

    @pytest.mark.asyncio
    async def test_get_playlist_if_not_exists(
        self,
        filled_playlists,
        filled_playlists_in_memory_reader,
        fake_uow,
    ):
        with pytest.raises(PlaylistNotFoundException):
            await GetPlaylistHandler(
                filled_playlists_in_memory_reader, fake_uow
            ).execute(GetPlaylistCommand(uuid.uuid4()))

    @pytest.mark.asyncio
    async def test_get_song(
        self,
        filled_playlists,
        filled_playlists_in_memory_reader,
        fake_uow,
        songs_id,
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]

        song_from_handler = await GetSongHandler(
            filled_playlists_in_memory_reader, fake_uow
        ).execute(GetSongCommand(playlist.id, songs_id[0]))

        assert song_from_handler is not None

    @pytest.mark.asyncio
    async def test_update_song(
        self,
        filled_cache_playlists_data,
        filled_playlists_cache,
        filled_playlists,
        filled_playlists_in_memory_repo,
        fake_uow,
        songs_id,
    ):
        playlist: Playlist = list(filled_playlists.items())[0][1]
        playlist_from_cache: Playlist = list(
            filled_cache_playlists_data.items()
        )[0][1]
        song_id: Song = songs_id[0]

        old_song = playlist.get_song(song_id)
        old_song_from_cache = playlist_from_cache.get_song(song_id)

        await UpdateSongHandler(
            filled_playlists_in_memory_repo,
            filled_playlists_cache,
            fake_uow,
        ).execute(UpdateSongCommand(playlist.id, Song("title", 123, song_id)))

        new_song = playlist.get_song(song_id)

        assert new_song is not None
        assert new_song.title != old_song.title
        assert new_song.id == old_song.id
        assert new_song.duration != old_song.duration

        assert new_song.title != old_song_from_cache.title
        assert new_song.id == old_song_from_cache.id
        assert new_song.duration != old_song_from_cache.duration
