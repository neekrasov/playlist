import logging
from grpc.aio import ServerInterceptor

from playlist.domain.exceptions import PlaylistException, NotFoundException
from .exc_handlers import handle_not_found_error, handle_playlist_error


class LoggingInterceptor(ServerInterceptor):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    async def intercept_service(self, continuation, client_call_details):
        self._logger.info(f"Called {client_call_details.method}")
        return await continuation(client_call_details)


class ErrorHandlerInterceptor(ServerInterceptor):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    async def intercept_service(self, continuation, client_call_details):
        try:
            return await continuation(client_call_details)
        except PlaylistException as e:
            self._logger.exception(e)
            return handle_playlist_error(e)
        except NotFoundException as e:
            self._logger.exception(e)
            return handle_not_found_error(e)
