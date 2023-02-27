import logging
import uuid
from grpc.aio import ServicerContext

from ..generated.playlist_pb2 import (
    CreatePlaylistRequest,
    CreatePlaylistResponse,
    DeletePlaylistRequest,
    DeletePlaylistResponse,
    GetPlaylistRequest,
    GetPlaylistResponse,
)
from ..generated.playlist_pb2_grpc import PlayListServicer
from ...di.container import inject, DIMixin
from common.mediator import Mediator
from playlist.domain.entities import PlaylistID
from playlist.application.handlers.delete_playlist import DeletePlaylistCommand
from playlist.application.handlers.create_playlist import CreatePlaylistCommand
from playlist.application.handlers.get_playlist import (
    GetPlaylistCommand,
    GetPlaylistDTO,
)

logger = logging.getLogger(__name__)


class PlaylistService(PlayListServicer, DIMixin):
    @inject(CreatePlaylistRequest)
    async def CreatePlaylist(  # type: ignore
        self,
        request: CreatePlaylistRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> CreatePlaylistResponse:
        playlist_id = await mediator.send(CreatePlaylistCommand(request.title))
        return CreatePlaylistResponse(id=playlist_id.bytes)

    @inject(DeletePlaylistRequest)
    async def DeletePlaylist(  # type: ignore
        self,
        request: DeletePlaylistRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> DeletePlaylistResponse:
        uuid_ = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        await mediator.send(DeletePlaylistCommand(uuid_))
        return DeletePlaylistResponse()

    @inject(GetPlaylistRequest)
    async def GetPlaylist(  # type: ignore
        self,
        request: GetPlaylistRequest,
        context: ServicerContext,
        mediator: Mediator,
    ) -> GetPlaylistResponse:
        uuid_ = PlaylistID(uuid.UUID(bytes=request.playlist_id))
        playlist: GetPlaylistDTO = await mediator.send(
            GetPlaylistCommand(uuid_)
        )
        return GetPlaylistResponse(
            playlist_id=playlist.id.bytes,
            title=playlist.title,
            state=playlist.status.value,
        )
