import uuid
import pytest
import asyncio

from playlist.domain.entities import Playlist, Song, SongID, PlaylistID


class TestPlaylistCache:
    def test_delete(self, playlists_cache, cache_playlists_data):
        id_ = PlaylistID(uuid.uuid4())
        playlist = Playlist("test", id_)
        playlists_cache.add_playlist(playlist)
        playlists_cache.delete_playlist(id_)
        assert cache_playlists_data.get(playlist.id) is None

    def test_add(self, playlists_cache, cache_playlists_data):
        playlist = Playlist("test", PlaylistID(uuid.uuid4()))
        playlists_cache.add_playlist(playlist)
        assert cache_playlists_data.get(playlist.id) == playlist

    @pytest.mark.asyncio
    async def test_clean_playlist_before_playing(
        self, playlists_cache, cache_playlists_data
    ):
        playlist = Playlist("test", PlaylistID(uuid.uuid4()))
        playlist.add_song(Song("test", 1, SongID(uuid.uuid4())))
        playlists_cache.add_playlist(playlist)

        await asyncio.gather(playlist.play(), playlists_cache.check(playlist))

        assert cache_playlists_data.get(playlist.id) is None
