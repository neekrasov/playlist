from typing import Dict, Callable, TypeVar, Type
from dataclasses import dataclass
from functools import partial
from di import Container, bind_by_type, ScopeState
from di.executors import AsyncExecutor
from di.dependent import Dependent
from grpc.aio import ServicerContext
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)

from playlist.config import Settings
from playlist.domain.entities import PlaylistID, Playlist
from playlist.adapters.sqlalchemy.factories import (
    build_sa_session_factory,
    build_sa_session,
    build_sa_engine,
)
from playlist.adapters.sqlalchemy.repo import (
    PlaylistRepositoryImpl,
    PlaylistRepository,
)
from playlist.adapters.sqlalchemy.reader import (
    PlaylistReaderImpl,
    PlaylistReader,
)
from playlist.adapters.sqlalchemy.uow import (
    UnitOfWorkImpl,
    UnitOfWork,
)
from playlist.adapters.memory.cache import PlaylistCache, InMemoryPlaylistCache
from playlist.adapters.mediator import Mediator
from ..mediator.factory import build_mediator

MessageType = TypeVar("MessageType")


class DIMixin:
    def __init__(self, container: Container, app_state: ScopeState):
        self._container = container
        self._app_state = app_state


@dataclass
class DIScope:
    APP = "app"
    REQUEST = "request"


def inject(
    message_type: Type[MessageType],
) -> Callable[[Callable], Callable]:
    def wrapper(func: Callable) -> Callable:
        async def handler(
            self, request: MessageType, context: ServicerContext
        ) -> Callable:
            async with self._container.enter_scope(
                DIScope.REQUEST, self._app_state
            ) as request_state:
                solved = self._container.solve(
                    Dependent(partial(func, self=self), scope=DIScope.REQUEST),
                    scopes=[DIScope.APP, DIScope.REQUEST],
                )
                return await solved.execute_async(
                    AsyncExecutor(),
                    request_state,
                    values={
                        message_type: request,
                        ServicerContext: context,
                    },
                )

        return handler

    return wrapper


def build_container() -> Container:
    container = Container()
    cache_playlists: Dict[PlaylistID, Playlist] = {}
    cache = InMemoryPlaylistCache(cache_playlists)

    container.bind(
        bind_by_type(
            Dependent(lambda *args: Settings(), scope=DIScope.APP), Settings
        )
    )
    container.bind(
        bind_by_type(
            Dependent(build_sa_engine, scope=DIScope.APP), AsyncEngine
        )
    )
    container.bind(
        bind_by_type(
            Dependent(build_sa_session_factory, scope=DIScope.APP),
            async_sessionmaker[AsyncSession],
        )
    )
    container.bind(
        bind_by_type(
            Dependent(
                lambda *args: cache,
                scope=DIScope.APP,
            ),
            PlaylistCache,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(build_sa_session, scope=DIScope.REQUEST), AsyncSession
        )
    )
    container.bind(
        bind_by_type(
            Dependent(PlaylistReaderImpl, scope=DIScope.REQUEST),
            PlaylistReader,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(PlaylistRepositoryImpl, scope=DIScope.REQUEST),
            PlaylistRepository,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UnitOfWorkImpl, scope=DIScope.REQUEST), UnitOfWork
        )
    )
    container.bind(
        bind_by_type(
            Dependent(build_mediator, scope=DIScope.REQUEST), Mediator
        )
    )

    return container
