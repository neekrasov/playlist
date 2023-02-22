import asyncio
from enum import Enum
from typing import Optional
from dataclasses import dataclass

from .exceptions import PlayListException


class PlayListState(Enum):
    PLAYING = asyncio.Event()
    PAUSED = asyncio.Event()
    STOPPED = asyncio.Event()
    NEXT = asyncio.Event()


@dataclass
class Song:
    id: int
    title: str
    duration: float

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class PlayListNode:
    song: Song
    next: Optional["PlayListNode"] = None
    prev: Optional["PlayListNode"] = None

    track: float = 0.0

    async def play(self) -> PlayListState:
        # print(self.song.title, self.track)
        if self.track == self.song.duration:
            # print(f"# track {self.song.title} ended")
            return PlayListState.NEXT
        self.track += 1
        await asyncio.sleep(1)
        return PlayListState.PLAYING


class PlayList:
    def __init__(self, title: str):
        self.title = title
        self.head: Optional[PlayListNode] = None
        self.tail: Optional[PlayListNode] = None
        self.current: Optional[PlayListNode] = None
        self.state: Optional[PlayListState] = None
        self.size: int = 0

    def add_song(self, song: Song) -> None:
        node = PlayListNode(song)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

        if self.state != PlayListState.PLAYING:
            self.current = self.tail

        self.size += 1

    def remove_song(self, song: Song) -> None:
        if self.state == PlayListState.PLAYING and self.current.song == song:
            raise PlayListException("Cannot remove song while playing")

        node = self._get_node(song.id)

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
            raise PlayListException(f"Song with id {song.id} not found")

    def _get_node(self, song_id: int) -> Optional[PlayListNode]:
        node = self.head
        while node is not None and node.song.id != song_id:
            node = node.next
        return node

    async def play(self) -> PlayListState:
        self.state = PlayListState.PLAYING
        await self._play()

    async def _play(self) -> None:
        while self._check_playback_stop():
            self.state = await self.current.play()
            self.state.value.set()

        if PlayListState.NEXT.value.is_set():
            if self.current.prev:
                PlayListState.PLAYING.value.set()
                PlayListState.NEXT.value.clear()
                self.state = PlayListState.PLAYING
                self.current = self.current.prev
                await self._play()
            else:
                PlayListState.NEXT.value.clear()
                PlayListState.PLAYING.value.clear()
                self.state = PlayListState.STOPPED

        elif PlayListState.STOPPED.value.is_set():
            PlayListState.PLAYING.value.clear()
            self.state = PlayListState.STOPPED

    def _check_playback_stop(self) -> bool:
        return (
            self.current
            and not PlayListState.NEXT.value.is_set()
            and not PlayListState.STOPPED.value.is_set()
            and not PlayListState.PAUSED.value.is_set()
        )

    def pause(self) -> None:
        self.state = PlayListState.PAUSED
        PlayListState.STOPPED.value.clear()
        PlayListState.PLAYING.value.clear()
        PlayListState.PAUSED.value.set()

    async def resume(self) -> None:
        self.state = PlayListState.PLAYING
        PlayListState.PAUSED.value.clear()
        PlayListState.STOPPED.value.clear()
        await self._play()

    def next(self) -> None:
        if self.current.prev:
            self.current = self.current.prev
        else:
            self.current = self.tail

    def prev(self) -> None:
        if self.current.next:
            self.current = self.current.next
        else:
            self.current = self.head
        self.current.track = 0.0  # reset track
