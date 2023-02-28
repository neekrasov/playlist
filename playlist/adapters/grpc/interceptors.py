import logging
from grpc.aio import ServerInterceptor


class LoggingInterceptor(ServerInterceptor):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    async def intercept_service(self, continuation, client_call_details):
        self._logger.info(f"Called {client_call_details.method}")
        return await continuation(client_call_details)
