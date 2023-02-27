import asyncio
import logging
import logging.config
from grpc.aio import server

from playlist.config import Settings
from .generated import playlist_pb2_grpc as playlist_servicers
from .services import PlaylistService
from ..di.container import build_container, DIScope
from .interceptors import LoggingInterceptor, ErrorHandlerInterceptor
from ..sqlalchemy.models import start_mapping


async def serve(socket: str) -> None:
    container = build_container()
    async with container.enter_scope(DIScope.APP) as app_state:
        grpc_server = server(
            interceptors=[
                ErrorHandlerInterceptor(logger),
                LoggingInterceptor(logger),
            ]
        )
        playlist_servicers.add_PlayListServicer_to_server(
            PlaylistService(container, app_state), grpc_server
        )

        logger.info(f"Serve on {socket}")
        grpc_server.add_insecure_port(socket)

        await grpc_server.start()
        try:
            await grpc_server.wait_for_termination()
        finally:
            await grpc_server.stop(0)


if __name__ == "__main__":
    settings = Settings()
    logging.config.fileConfig("playlist/config/logging_config.ini")
    logger = logging.getLogger(__name__)
    start_mapping()

    try:
        asyncio.run(serve(settings.grpc.socket))
    except KeyboardInterrupt:
        pass
