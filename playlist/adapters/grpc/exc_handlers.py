from grpc import StatusCode, ServicerContext

from playlist.domain.exceptions import PlaylistException, NotFoundException


def error_handler(func):
    async def wrapper(self, request, context: ServicerContext):
        try:
            return await func(self, request, context)
        except NotFoundException as e:
            await context.abort(StatusCode.NOT_FOUND, e.message)
        except PlaylistException as e:
            await context.abort(StatusCode.ABORTED, e.message)

    return wrapper
