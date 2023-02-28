from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NextSongRequest(_message.Message):
    __slots__ = ["playlist_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    def __init__(self, playlist_id: _Optional[bytes] = ...) -> None: ...

class NextSongResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PauseSongRequest(_message.Message):
    __slots__ = ["playlist_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    def __init__(self, playlist_id: _Optional[bytes] = ...) -> None: ...

class PauseSongResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PlaySongRequest(_message.Message):
    __slots__ = ["playlist_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    def __init__(self, playlist_id: _Optional[bytes] = ...) -> None: ...

class PlaySongResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PrevSongRequest(_message.Message):
    __slots__ = ["playlist_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    def __init__(self, playlist_id: _Optional[bytes] = ...) -> None: ...

class PrevSongResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
