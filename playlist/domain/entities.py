import asyncio
import uuid
from enum import Enum, auto
from typing import Optional, NewType
from dataclasses import dataclass

from .exceptions import PlayListException

SongID = NewType("SongID", uuid.UUID)
PlaylistID = NewType("PlaylistID", uuid.UUID)


class PlaylistState(Enum):
    PLAYING = auto()
    PAUSED = auto()
    STOPPED = auto()
    NEXT = auto()


@dataclass
class Song:
    title: str
    duration: float
    id: Optional[SongID] = None

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
    def __init__(self, title: str, id: Optional[PlaylistID] = None):
        self.id = id
        self.title = title
        self.head: Optional[PlaylistNode] = None
        self.tail: Optional[PlaylistNode] = None
        self.current: Optional[PlaylistNode] = None
        self.state: Optional[PlaylistState] = None
        self.size: int = 0

    def add_song(self, song: Song) -> None:
        node = PlaylistNode(song)
        if self.head is None:
            self.head = node
        else:
            node.prev = self.tail
            if self.tail:
                self.tail.next = node

        self.tail = node

        if self.state != PlaylistState.PLAYING:
            self.current = self.tail

        self.size += 1

    def remove_song(self, song_id: SongID) -> None:
        if (
            self.current
            and self.state == PlaylistState.PLAYING
            and self.current.song.id == song_id
        ):
            raise PlayListException("Cannot remove song while playing")

        node = self._get_node(song_id)

        if node is not None:
            if node.prev is not None:
                node.prev.next = node.next
            else:
                self.head = node.next
            if node.next is not None:
                node.next.prev = node.prev
            else:
                self.tail = node.prev
            self.size -= 1
        else:
            raise PlayListException(f"Song with id {song_id} not found")

    def _get_node(self, song_id: SongID) -> Optional[PlaylistNode]:
        node = self.head
        while node is not None and node.song.id != song_id:
            node = node.next
        return node

    async def play(self) -> None:
        self.state = PlaylistState.PLAYING
        await self._play()

    async def _play(self) -> None:
        while self.current and self._check_playback_stop():
            state = await self.current.play()
            if state:
                self.state = state

        if self.current and self.state == PlaylistState.NEXT:
            if self.current.prev:
                self.state = PlaylistState.PLAYING
                self.current = self.current.prev
                await self._play()
            else:
                self.state = PlaylistState.STOPPED

    def _check_playback_stop(self) -> bool:
        return (
            self.state != PlaylistState.NEXT
            and self.state != PlaylistState.STOPPED
            and self.state != PlaylistState.PAUSED
        )

    def pause(self) -> None:
        self.state = PlaylistState.PAUSED

    def next(self) -> None:
        if not self.current:
            raise PlayListException("Cannot move to next song")

        if self.current.prev:
            self.current = self.current.prev
        else:
            self.current = self.tail

    def prev(self) -> None:
        if not self.current:
            raise PlayListException("Cannot move to previous song")

        if self.current.next:
            self.current = self.current.next
        else:
            self.current = self.head

        if self.current:
            self.current.track = 0.0  # reset track

    def get_song(self, song_id: SongID) -> Optional[Song]:
        node = self._get_node(song_id)
        if node is None:
            return None
        return node.song

    def update_song(self, song: Song) -> None:
        if not song.id:
            raise PlayListException("Cannot update song without id")

        node = self._get_node(song.id)
        if node is None:
            raise PlayListException(f"Song with id {song.id} not found")
        node.song = song
