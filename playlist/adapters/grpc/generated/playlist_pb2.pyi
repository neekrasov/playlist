from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePlaylistRequest(_message.Message):
    __slots__ = ["title"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: str
    def __init__(self, title: _Optional[str] = ...) -> None: ...

class CreatePlaylistResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: bytes
    def __init__(self, id: _Optional[bytes] = ...) -> None: ...

class DeletePlaylistRequest(_message.Message):
    __slots__ = ["playlist_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    def __init__(self, playlist_id: _Optional[bytes] = ...) -> None: ...

class DeletePlaylistResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPlaylistRequest(_message.Message):
    __slots__ = ["playlist_id"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    def __init__(self, playlist_id: _Optional[bytes] = ...) -> None: ...

class GetPlaylistResponse(_message.Message):
    __slots__ = ["playlist_id", "state", "title"]
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    playlist_id: bytes
    state: str
    title: str
    def __init__(self, playlist_id: _Optional[bytes] = ..., title: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...
