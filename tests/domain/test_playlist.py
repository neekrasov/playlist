import asyncio
import pytest
from playlist.domain.entities import PlayList, Song, PlayListState
from playlist.domain.exceptions import PlayListException


class TestPlaylist:
    def test_create_playlist(self):
        playlist = PlayList("test")
        assert playlist.title == "test"

    def test_add_song_to_playlist(self):
        playlist = PlayList("test")
        song = Song(1, "test", 1.0)
        playlist.add_song(song)
        assert playlist.size == 1
        assert playlist.head.song == song
        assert playlist.head == playlist.tail

    def test_add_many_songs_to_playlist(self):
        playlist = PlayList("test")
        song1 = Song(1, "test", 1.0)
        song2 = Song(2, "test", 1.0)
        playlist.add_song(song1)
        playlist.add_song(song2)
        assert playlist.size == 2
        assert playlist.head.song == song1
        assert playlist.tail.song == song2

    def test_remove_one_song_from_playlist(self):
        playlist = PlayList("test")
        song = Song(1, "test", 1.0)
        playlist.add_song(song)
        playlist.remove_song(song)
        assert playlist.size == 0
        assert playlist.head is None
        assert playlist.tail is None

    def test_remove_after_many_add_songs_from_playlist(self):
        playlist = PlayList("test")
        song1 = Song(1, "test", 1.0)
        song2 = Song(2, "test", 1.0)
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.remove_song(song1)
        assert playlist.size == 1
        assert playlist.head.song == song2
        assert playlist.tail.song == song2

    @pytest.mark.asyncio
    async def test_play(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 1.0)
        song2 = Song(2, "test2", 1.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        await playlist.play()
        assert playlist.state == PlayListState.STOPPED
        assert playlist.size == 2
        assert playlist.head.song == song1
        assert playlist.tail.song == song2

    @pytest.mark.asyncio
    async def test_pause(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 1.0)
        song2 = Song(2, "test2", 2.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        async def pause():
            await asyncio.sleep(0.5)
            print("pause called")
            playlist.pause()

            assert playlist.state == PlayListState.PAUSED

        await asyncio.gather(playlist.play(), pause())

    @pytest.mark.asyncio
    async def test_pause_with_resume(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 1.0)
        song2 = Song(2, "test2", 2.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        assert playlist.current.song == song2

        async def stop():
            await asyncio.sleep(1)
            print("pause called")
            playlist.pause()

            assert playlist.current.song == song2

        async def resume():
            await asyncio.sleep(2)
            print("pause finished")
            print("resume called")
            await playlist.resume()
            assert playlist.current.song == song1

        await asyncio.gather(playlist.play(), stop(), resume())

    @pytest.mark.asyncio
    async def test_pause_track(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 1.0)
        song2 = Song(2, "test2", 3.0)
        playlist.add_song(song1)
        playlist.add_song(song2)

        start_track = 0

        async def stop():
            global start_track
            await asyncio.sleep(2)
            print("pause called")
            playlist.pause()
            start_track = playlist.current.track

            assert playlist.current.song == song2

        async def resume():
            global start_track
            await asyncio.sleep(3)
            print("pause finished")
            print("resume called")
            assert playlist.current.track == start_track
            await playlist.resume()
            assert playlist.current.song == song1

        await asyncio.gather(playlist.play(), stop(), resume())

    @pytest.mark.asyncio
    async def test_next(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 1.0)
        song2 = Song(2, "test2", 100.0)
        song3 = Song(3, "test3", 100.0)
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.add_song(song3)

        async def first_next():
            await asyncio.sleep(1)
            assert playlist.current.song == song3
            print("next called")
            playlist.next()

        async def second_next():
            await asyncio.sleep(2)
            assert playlist.current.song == song2
            print("next called")
            playlist.next()

            assert playlist.current.song == song1

        await asyncio.gather(playlist.play(), first_next(), second_next())

    @pytest.mark.asyncio
    async def test_previous(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 10.0)
        song2 = Song(2, "test2", 2.0)
        song3 = Song(3, "test3", 1.0)
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.add_song(song3)

        async def previous():
            await asyncio.sleep(4)
            assert playlist.current.song == song1
            print("previous called")
            playlist.prev()
            assert playlist.current.song == song2
            await asyncio.sleep(2)
            print("paused called")
            playlist.pause()

        await asyncio.gather(playlist.play(), previous())

    @pytest.mark.asyncio
    async def test_add_song_with_play(self):
        playlist = PlayList("test")
        song1 = Song(1, "test1", 5.0)
        song2 = Song(2, "test2", 5.0)
        playlist.add_song(song1)

        # Только что добавленный трек не должен воспроизводиться сразу же
        # т.к он добавляется в хвост, а порядок идёт от хвоста к голове
        async def add_song_with_play():
            await asyncio.sleep(1)
            assert playlist.current.song == song1
            print("add_song_with_play called")
            playlist.add_song(song2)
            assert playlist.current.song == song1
            assert playlist.size == 2
            assert playlist.tail.song == song2
            await asyncio.sleep(2)
            print("paused called")
            playlist.pause()

        await asyncio.gather(playlist.play(), add_song_with_play())


class TestPlayListErrors:
    @pytest.mark.asyncio
    async def test_remove_playing_song(self):
        with pytest.raises(PlayListException):
            playlist = PlayList("test")
            song1 = Song(1, "test1", 5.0)
            song2 = Song(2, "test2", 5.0)
            playlist.add_song(song1)
            playlist.add_song(song2)

            async def remove_playing_song():
                await asyncio.sleep(1)
                print("remove_playing_song called")
                playlist.remove_song(song2)

            await asyncio.gather(playlist.play(), remove_playing_song())
