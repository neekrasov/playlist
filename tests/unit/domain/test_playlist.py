import asyncio
import pytest
import uuid
from playlist.domain.entities import Playlist, Song, PlaylistState, SongID
from playlist.domain.exceptions import PlaylistException


class TestPlaylist:
    def test_create_playlist(self):
        playlist = Playlist("test")
        assert playlist.title == "test"

    def test_add_song_to_playlist(self):
        playlist = Playlist("test")
        song = Song("test", 1.0, uuid.uuid4())
        playlist.add_song(song)
        assert playlist.size == 1
        assert playlist.head.song == song
        assert playlist.head == playlist.tail

    def test_add_many_songs_to_playlist(self):
        playlist = Playlist("test")
        song1 = Song("test", 1.0, uuid.uuid4())
        song2 = Song("test", 1.0, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)
        assert playlist.size == 2
        assert playlist.head.song == song1
        assert playlist.tail.song == song2

    def test_remove_one_song_from_playlist(self):
        playlist = Playlist("test")
        sond_id = uuid.uuid4()
        song = Song("test", 1.0, sond_id)
        playlist.add_song(song)
        playlist.remove_song(sond_id)
        assert playlist.size == 0
        assert playlist.head is None
        assert playlist.tail is None

    def test_remove_after_many_add_songs_from_playlist(self):
        playlist = Playlist("test")
        song1 = Song("test", 1.0, uuid.uuid4())
        song2 = Song("test", 1.0, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.remove_song(song1.id)
        assert playlist.size == 1
        assert playlist.head.song == song2
        assert playlist.tail.song == song2

    def test_get_song(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0, uuid.uuid4())
        song2 = Song("test2", 1.0, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)
        assert playlist.get_song(song1.id) == song1

    def test_get_non_existing_song(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0, uuid.uuid4())
        song2 = Song("test2", 1.0, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)
        assert playlist.get_song(uuid.uuid4()) is None

    def test_update_song(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0, uuid.uuid4())
        song2 = Song("test2", 1.0, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)
        update_song = Song("test2", 2.0, song2.id)
        playlist.update_song(update_song)
        assert playlist.get_song(song2.id) == update_song

    @pytest.mark.asyncio
    async def test_pause_not_playing(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0, uuid.uuid4())
        song2 = Song("test2", 1.0, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)
        with pytest.raises(PlaylistException):
            await playlist.pause()

    @pytest.mark.asyncio
    async def test_play(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0)
        song2 = Song("test2", 1.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        await playlist.play()
        assert playlist._state == PlaylistState.STOPPED
        assert playlist.size == 2
        assert playlist.head.song == song1
        assert playlist.tail.song == song2

    @pytest.mark.asyncio
    async def test_pause(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0)
        song2 = Song("test2", 100.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        async def stop():
            await asyncio.sleep(1.5)
            assert playlist._state == PlaylistState.PAUSED
            playlist.stop()

        async def pause():
            await asyncio.sleep(1)
            await playlist.pause()

        await asyncio.gather(playlist.play(), pause(), stop())

    @pytest.mark.asyncio
    async def test_update_playing_song(self):
        playlist = Playlist("test")
        update_uuid = SongID(uuid.uuid4())
        song1 = Song("test1", 1.0)
        song2 = Song("test2", 100.0, update_uuid)
        playlist.add_song(song1)
        playlist.add_song(song2)

        async def update():
            await asyncio.sleep(1)
            playlist.update_song(Song("test2", 2.0, update_uuid))

        with pytest.raises(PlaylistException):
            await asyncio.gather(playlist.play(), update())

    @pytest.mark.asyncio
    async def test_pause_with_resume(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0)
        song2 = Song("test2", 3.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        assert playlist._current.song == song2

        async def stop():
            await asyncio.sleep(1)
            await playlist.pause()

            assert playlist._current.song == song2

        async def resume():
            await asyncio.sleep(2)
            await playlist.play()
            assert playlist._current.song == song1

        await asyncio.gather(playlist.play(), stop(), resume())

    @pytest.mark.asyncio
    async def test_pause_track(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0)
        song2 = Song("test2", 3.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        start_track = 0

        async def stop():
            global start_track
            await asyncio.sleep(1)
            await playlist.pause()
            start_track = playlist._current.track

            assert playlist._current.song == song2

        async def resume():
            global start_track
            await asyncio.sleep(3)
            assert playlist._current.track == start_track
            await playlist.play()
            assert playlist._current.song == song1

        await asyncio.gather(playlist.play(), stop(), resume())

    @pytest.mark.asyncio
    async def test_next(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1.0)
        song2 = Song("test2", 100.0)
        song3 = Song("test3", 100.0)
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.add_song(song3)

        async def first_next():
            await asyncio.sleep(1)
            assert playlist._current.song == song3
            playlist.next()

        async def second_next():
            await asyncio.sleep(2)
            assert playlist._current.song == song2
            playlist.next()

            assert playlist._current.song == song1

        await asyncio.gather(playlist.play(), first_next(), second_next())

    @pytest.mark.asyncio
    async def test_previous(self):
        playlist = Playlist("test")
        song1 = Song("test1", 10.0)
        song2 = Song("test2", 2.0)
        song3 = Song("test3", 1.0)
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.add_song(song3)

        async def previous():
            await asyncio.sleep(4)
            assert playlist._current.song == song1
            playlist.prev()
            assert playlist._current.song == song2
            await asyncio.sleep(1)
            playlist.stop()

        await asyncio.gather(playlist.play(), previous())

    @pytest.mark.asyncio
    async def test_add_song_with_play(self):
        playlist = Playlist("test")
        song1 = Song("test1", 5.0)
        song2 = Song("test2", 5.0)
        playlist.add_song(song1)

        # Только что добавленный трек не должен воспроизводиться сразу же
        # т.к он добавляется в хвост, а порядок идёт от хвоста к голове
        async def add_song_with_play():
            await asyncio.sleep(1)
            assert playlist._current.song == song1
            playlist.add_song(song2)
            assert playlist._current.song == song1
            assert playlist.size == 2
            assert playlist.tail.song == song2
            await asyncio.sleep(2)
            playlist.stop()

        await asyncio.gather(playlist.play(), add_song_with_play())


class TestPlayListErrors:
    def test_update_non_existing_song(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1)
        song2 = Song("test2", 2)
        playlist.add_song(song1)
        playlist.add_song(song2)
        with pytest.raises(PlaylistException):
            playlist.update_song(Song(uuid.uuid4(), "test3", 1.0))

    @pytest.mark.asyncio
    async def test_double_play(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1, uuid.uuid4())
        song2 = Song("test2", 5, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)

        async def double_play():
            await asyncio.sleep(2)
            with pytest.raises(PlaylistException):
                await playlist.play()
            assert playlist.is_playing is True

        await asyncio.gather(playlist.play(), double_play())

    @pytest.mark.asyncio
    async def test_remove_playing_song(self):
        with pytest.raises(PlaylistException):
            playlist = Playlist("test")
            song1 = Song("test1", 1, uuid.uuid4())
            song2 = Song("test2", 2, uuid.uuid4())
            playlist.add_song(song1)
            playlist.add_song(song2)

            async def remove_playing_song():
                await asyncio.sleep(1)
                playlist.remove_song(song2.id)

            await asyncio.gather(playlist.play(), remove_playing_song())

    @pytest.mark.asyncio
    async def test_update_song_without_id(self):
        playlist = Playlist("test")
        song1 = Song("test1", 1, uuid.uuid4())
        song2 = Song("test2", 2, uuid.uuid4())
        playlist.add_song(song1)
        playlist.add_song(song2)

        with pytest.raises(PlaylistException):
            playlist.update_song(Song("test3", 1))
