import uuid
import asyncio
import logging
import logging.config

from grpc.aio import (
    ServerInterceptor,
    ServicerContext,
)
from grpc.aio import server

from playlist.config import Settings
from .servicers import (
    playlist_pb2 as playlist_messages,
    playlist_pb2_grpc as playlist_service,
)


class LoggingInterceptor(ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        logger.info(
            f"Received request: {handler_call_details.method} \
            ({handler_call_details.invocation_metadata})"
        )

        try:
            response = await continuation(handler_call_details)
            logger.info(f"Sending response: {response}")
            return response
        except Exception as e:
            logger.exception(e)
            raise


class PLaylistService(playlist_service.PlayListServicer):
    async def CreatePlaylist(
        self,
        request: playlist_messages.CreatePlaylistRequest,
        context: ServicerContext,
    ):
        return playlist_messages.CreatePlaylistResponse(id=uuid.uuid4().bytes)


async def serve(socket: str) -> None:
    grpc_server = server(interceptors=[LoggingInterceptor()])
    playlist_service.add_PlayListServicer_to_server(
        PLaylistService(), grpc_server
    )
    logger.info(f"Serve on {socket}")

    grpc_server.add_insecure_port(socket)

    await grpc_server.start()
    try:
        await grpc_server.wait_for_termination()
    finally:
        await grpc_server.stop(None)


if __name__ == "__main__":
    settings = Settings()
    logging.config.fileConfig("playlist/config/logging_config.ini")
    logger = logging.getLogger(__name__)

    try:
        asyncio.run(serve(settings.grpc.socket))
    except KeyboardInterrupt:
        pass
