from typing import Protocol, AsyncContextManager


class UnitOfWork(Protocol):
    @property
    def pipeline(self) -> AsyncContextManager:
        ...

    async def commit(self) -> None:
        ...
