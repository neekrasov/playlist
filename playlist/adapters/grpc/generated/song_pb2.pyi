from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSongRequest(_message.Message):
    __slots__ = ["playlist_id", "song"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    SONG_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    song: SongMessage
    def __init__(
        self,
        playlist_id: _Optional[bytes] = ...,
        song: _Optional[_Union[SongMessage, _Mapping]] = ...,
    ) -> None: ...

class CreateSongResponse(_message.Message):
    __slots__ = ["song_id"]
    SONG_ID_FIELD_NUMBER: _ClassVar[int]
    song_id: bytes
    def __init__(self, song_id: _Optional[bytes] = ...) -> None: ...

class DeleteSongRequest(_message.Message):
    __slots__ = ["playlist_id", "song_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    SONG_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    song_id: bytes
    def __init__(
        self,
        playlist_id: _Optional[bytes] = ...,
        song_id: _Optional[bytes] = ...,
    ) -> None: ...

class DeleteSongResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSongRequest(_message.Message):
    __slots__ = ["playlist_id", "song_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    SONG_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    song_id: bytes
    def __init__(
        self,
        playlist_id: _Optional[bytes] = ...,
        song_id: _Optional[bytes] = ...,
    ) -> None: ...

class GetSongResponse(_message.Message):
    __slots__ = ["song", "song_id"]
    SONG_FIELD_NUMBER: _ClassVar[int]
    SONG_ID_FIELD_NUMBER: _ClassVar[int]
    song: SongMessage
    song_id: bytes
    def __init__(
        self,
        song_id: _Optional[bytes] = ...,
        song: _Optional[_Union[SongMessage, _Mapping]] = ...,
    ) -> None: ...

class SongMessage(_message.Message):
    __slots__ = ["duration", "title"]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    duration: float
    title: str
    def __init__(
        self, title: _Optional[str] = ..., duration: _Optional[float] = ...
    ) -> None: ...

class UpdateSongRequest(_message.Message):
    __slots__ = ["playlist_id", "song", "song_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    SONG_FIELD_NUMBER: _ClassVar[int]
    SONG_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    song: SongMessage
    song_id: bytes
    def __init__(
        self,
        playlist_id: _Optional[bytes] = ...,
        song_id: _Optional[bytes] = ...,
        song: _Optional[_Union[SongMessage, _Mapping]] = ...,
    ) -> None: ...

class UpdateSongResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
