import asyncio
import uuid
import datetime
from enum import Enum
from typing import Optional, NewType
from dataclasses import dataclass

from .exceptions import PlaylistException, SongNotFoundException

SongID = NewType("SongID", uuid.UUID)
PlaylistID = NewType("PlaylistID", uuid.UUID)


class PlaylistState(Enum):
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    NEXT = "NEXT"


@dataclass
class Song:
    title: str
    duration: float
    id: Optional[SongID] = None
    playlist_id: Optional[PlaylistID] = None
    timestamp: Optional[datetime.datetime] = None

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class PlaylistNode:
    song: Song
    next: Optional["PlaylistNode"] = None
    prev: Optional["PlaylistNode"] = None

    track: float = 0.0

    async def play(self) -> Optional[PlaylistState]:
        if self.track == self.song.duration:
            return PlaylistState.NEXT
        self.track += 1
        await asyncio.sleep(1)
        return None


class Playlist:
    def __init__(
        self,
        title: str,
        id: Optional[PlaylistID] = None,
        max_pause_time: float = 1.5,
    ):
        self.id = id
        self.title = title
        self._head: Optional[PlaylistNode] = None
        self._tail: Optional[PlaylistNode] = None
        self._current: Optional[PlaylistNode] = None
        self._state: PlaylistState = PlaylistState.STOPPED
        self._size: int = 0
        self._max_pause_time = max_pause_time

    def add_song(self, song: Song) -> None:
        node = PlaylistNode(song)
        if self._head is None:
            self._head = node
        else:
            node.prev = self._tail
            if self._tail:
                self._tail.next = node

        self._tail = node

        if self._state != PlaylistState.PLAYING:
            self._current = self._tail

        self._size += 1

    def remove_song(self, song_id: SongID) -> None:
        self._check_is_playing(song_id)

        node = self._get_node(song_id)

        if node is not None:
            if node.prev is not None:
                node.prev.next = node.next
            else:
                self._head = node.next
            if node.next is not None:
                node.next.prev = node.prev
            else:
                self._tail = node.prev
            self._size -= 1
        else:
            raise SongNotFoundException(song_id)

    def _check_is_playing(self, song_id: SongID) -> None:
        if (
            self._current
            and self._state == PlaylistState.PLAYING
            and self._current.song.id == song_id
        ):
            raise PlaylistException("Cannot remove song while playing")

    def _get_node(self, song_id: SongID) -> Optional[PlaylistNode]:
        node = self.head
        while node is not None and node.song.id != song_id:
            node = node.next
        return node

    async def play(self) -> None:
        if self._state == PlaylistState.PLAYING:
            raise PlaylistException("Playlist is already playing song")

        self._state = PlaylistState.PLAYING
        await self._play()

    async def _play(self) -> None:
        while self._current and self._check_playback_stop():
            state = await self._current.play()
            if state:
                self._state = state

        if self._current and self._state == PlaylistState.NEXT:
            if self._current.prev:
                self._state = PlaylistState.PLAYING
                self._current = self._current.prev
                await self._play()
            else:
                self._state = PlaylistState.STOPPED

    def _check_playback_stop(self) -> bool:
        return (
            self._state != PlaylistState.NEXT
            and self._state != PlaylistState.STOPPED
            and self._state != PlaylistState.PAUSED
        )

    async def pause(self) -> None:
        if self._state == PlaylistState.PLAYING:
            self._state = PlaylistState.PAUSED

            # ???????? ?????????? N ???????????? ???? ???????????????????? ????????????,
            # ???? ???????????????? ???????????? ???????????? ???? ??????????????????????????
            await asyncio.sleep(self._max_pause_time)
            if self._state == PlaylistState.PAUSED:
                self._state = PlaylistState.STOPPED
        else:
            raise PlaylistException("Cannot pause playlist while not playing")

    def next(self) -> None:
        if not self._current:
            raise PlaylistException("Cannot move to next song")

        if self._current.prev:
            self._current = self._current.prev
        else:
            self._current = self._tail

    def prev(self) -> None:
        if not self._current:
            raise PlaylistException("Cannot move to previous song")

        if self._current.next:
            self._current = self._current.next
        else:
            self._current = self.head

        if self._current:
            self._current.track = 0.0  # reset track

    def get_song(self, song_id: SongID) -> Optional[Song]:
        node = self._get_node(song_id)
        if node is None:
            return None
        return node.song

    def update_song(self, song: Song) -> None:
        if not song.id:
            raise PlaylistException("Cannot update song without id")
        self._check_is_playing(song.id)

        node = self._get_node(song.id)
        if node is None:
            raise PlaylistException(f"Song with id {song.id} not found")
        node.song = song

    def stop(self) -> None:
        if self._state != PlaylistState.STOPPED:
            self._state = PlaylistState.STOPPED
        else:
            raise PlaylistException("Cannot stop playlist while not playing")

    @property
    def is_playing(self) -> bool:
        return self._state == PlaylistState.PLAYING

    @property
    def is_stopped(self) -> bool:
        return self._state == PlaylistState.STOPPED

    @property
    def current_song(self) -> Optional[Song]:
        return self._current.song if self._current else None

    @property
    def size(self) -> int:
        return self._size

    @property
    def head(self) -> Optional[PlaylistNode]:
        return self._head

    @property
    def tail(self) -> Optional[PlaylistNode]:
        return self._tail

    @property
    def state(self) -> PlaylistState:
        return self._state
