import uuid
from grpc.aio import ServicerContext

from common.mediator import Mediator
from playlist.domain.entities import PlaylistID
from playlist.application.handlers.play_song import PlaySongCommand
from playlist.application.handlers.pause_song import PauseSongCommand
from playlist.application.handlers.next_song import NextSongCommand
from playlist.application.handlers.prev_song import PrevSongCommand
from ..generated.control_pb2_grpc import PlaylistControlServicer
from ..generated.control_pb2 import (
    PlaySongRequest,
    PlaySongResponse,
    PauseSongRequest,
    PauseSongResponse,
    NextSongRequest,
    NextSongResponse,
    PrevSongRequest,
    PrevSongResponse,
)
from ...di.container import inject, DIMixin
from ..exc_handlers import error_handler


class PlaylistControlService(PlaylistControlServicer, DIMixin):
    @error_handler
    @inject(PlaySongRequest)
    async def PlaySong(  # type: ignore
        self,
        request: PlaySongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> PlaySongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        await mediator.send(PlaySongCommand(playlist_id))
        return PlaySongResponse()

    @error_handler
    @inject(PauseSongRequest)
    async def PauseSong(  # type: ignore
        self,
        request: PauseSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> PauseSongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        await mediator.send(PauseSongCommand(playlist_id))
        return PauseSongResponse()

    @error_handler
    @inject(NextSongRequest)
    async def NextSong(  # type: ignore
        self,
        request: NextSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> NextSongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        await mediator.send(NextSongCommand(playlist_id))
        return NextSongResponse()

    @error_handler
    @inject(PrevSongRequest)
    async def PrevSong(  # type: ignore
        self,
        request: PrevSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> PrevSongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        await mediator.send(PrevSongCommand(playlist_id))
        return PrevSongResponse()
