from grpc import ServicerContext, StatusCode, RpcError

from .generated.exc_pb2 import PlaylistError
from playlist.domain.exceptions import PlaylistException, NotFoundException


def handle_playlist_error(
    e: PlaylistException, context: ServicerContext
) -> None:
    context.set_code(StatusCode.ABORTED)
    context.set_details(str(e))
    context.set_trailing_metadata(str(e))
    raise RpcError(PlaylistError(message=str(e)))


def handle_not_found_error(
    e: NotFoundException, context: ServicerContext
) -> None:
    context.set_code(StatusCode.NOT_FOUND)
    context.set_details(str(e))
    context.set_trailing_metadata(str(e))
    raise RpcError(PlaylistError(message=str(e)))
