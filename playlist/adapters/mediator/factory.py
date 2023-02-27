from .mediator import Mediator, MediatorImpl
from common.uow import UnitOfWork
from playlist.application.protocols import (
    PlaylistRepository,
    PlaylistCache,
    PlaylistReader,
)
from playlist.application.handlers.create_playlist import (
    CreatePlaylistCommand,
    CreatePlaylistHandler,
)
from playlist.application.handlers.create_song import (
    CreateSongCommand,
    CreateSongHandler,
)
from playlist.application.handlers.delete_playlist import (
    DeletePlaylistCommand,
    DeletePlaylistHandler,
)
from playlist.application.handlers.delete_song import (
    DeleteSongCommand,
    DeleteSongHandler,
)
from playlist.application.handlers.get_playlist import (
    GetPlaylistCommand,
    GetPlaylistHandler,
)
from playlist.application.handlers.get_song import (
    GetSongCommand,
    GetSongHandler,
)
from playlist.application.handlers.next_song import (
    NextSongCommand,
    NextSongHandler,
)
from playlist.application.handlers.pause_song import (
    PauseSongCommand,
    PauseSongHandler,
)
from playlist.application.handlers.play_song import (
    PlaySongCommand,
    PlaySongHandler,
)
from playlist.application.handlers.prev_song import (
    PrevSongCommand,
    PrevSongHandler,
)
from playlist.application.handlers.update_song import (
    UpdateSongCommand,
    UpdateSongHandler,
)


def build_mediator(
    playlist_repository: PlaylistRepository,
    playlist_cache: PlaylistCache,
    playlist_reader: PlaylistReader,
    uow: UnitOfWork,
) -> Mediator:
    mediator = MediatorImpl()

    mediator.bind(
        CreatePlaylistCommand, CreatePlaylistHandler(playlist_repository, uow)
    )
    mediator.bind(
        CreateSongCommand,
        CreateSongHandler(playlist_repository, playlist_cache, uow),
    )
    mediator.bind(
        DeletePlaylistCommand,
        DeletePlaylistHandler(playlist_repository, playlist_cache, uow),
    )
    mediator.bind(
        DeleteSongCommand,
        DeleteSongHandler(playlist_repository, playlist_cache, uow),
    )
    mediator.bind(
        GetPlaylistCommand,
        GetPlaylistHandler(playlist_reader, playlist_cache, uow),
    )
    mediator.bind(GetSongCommand, GetSongHandler(playlist_reader, uow))
    mediator.bind(NextSongCommand, NextSongHandler(playlist_cache))
    mediator.bind(PauseSongCommand, PauseSongHandler(playlist_cache))
    mediator.bind(
        PlaySongCommand, PlaySongHandler(playlist_reader, playlist_cache)
    )
    mediator.bind(PrevSongCommand, PrevSongHandler(playlist_cache))
    mediator.bind(
        UpdateSongCommand,
        UpdateSongHandler(playlist_repository, playlist_cache, uow),
    )
    return mediator
