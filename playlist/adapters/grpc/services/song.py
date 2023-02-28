import uuid
from grpc.aio import ServicerContext

from common.mediator import Mediator
from playlist.domain.entities import PlaylistID, SongID, Song
from playlist.application.handlers.create_song import CreateSongCommand
from playlist.application.handlers.get_song import GetSongCommand, GetSongDTO
from playlist.application.handlers.update_song import UpdateSongCommand
from playlist.application.handlers.delete_song import DeleteSongCommand
from ..generated.song_pb2_grpc import SongServicer
from ..generated.song_pb2 import (
    SongMessage,
    CreateSongRequest,
    CreateSongResponse,
    GetSongRequest,
    GetSongResponse,
    UpdateSongRequest,
    UpdateSongResponse,
    DeleteSongRequest,
    DeleteSongResponse,
)
from ...di.container import inject, DIMixin
from ..exc_handlers import error_handler


class SongService(SongServicer, DIMixin):
    @error_handler
    @inject(CreateSongRequest)
    async def CreateSong(  # type: ignore
        self,
        request: CreateSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> CreateSongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        song = Song(
            title=request.song.title,
            duration=request.song.duration,
            playlist_id=playlist_id,
        )
        song_id: SongID = await mediator.send(CreateSongCommand(song))
        return CreateSongResponse(song_id=song_id.bytes)

    @error_handler
    @inject(GetSongRequest)
    async def GetSong(  # type: ignore
        self,
        request: GetSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> GetSongResponse:
        song_id = SongID(uuid.UUID(bytes=request.song_id))
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        song: GetSongDTO = await mediator.send(
            GetSongCommand(playlist_id, song_id)
        )
        return GetSongResponse(
            song_id=song.id.bytes,
            song=SongMessage(
                title=song.title,
                duration=song.duration,
            ),
        )

    @error_handler
    @inject(UpdateSongRequest)
    async def UpdateSong(  # type: ignore
        self,
        request: UpdateSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> UpdateSongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        song = Song(
            id=SongID(uuid.UUID(bytes=request.song_id)),
            title=request.song.title,
            duration=request.song.duration,
            playlist_id=playlist_id,
        )
        await mediator.send(UpdateSongCommand(song))
        return UpdateSongResponse()

    @error_handler
    @inject(DeleteSongRequest)
    async def DeleteSong(  # type: ignore
        self,
        request: DeleteSongRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> DeleteSongResponse:
        playlist_id = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        song_id = SongID(uuid.UUID(bytes=request.song_id))
        await mediator.send(DeleteSongCommand(playlist_id, song_id))
        return DeleteSongResponse()
