import contextlib
from typing import AsyncGenerator, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from common.uow import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @contextlib.asynccontextmanager
    async def _transaction(self) -> AsyncGenerator:
        if not self._session.in_transaction() and self._session.is_active:
            async with self._session.begin() as transaction:
                yield transaction
        else:
            yield

    @property
    def pipeline(
        self,
    ) -> AsyncContextManager[AsyncSessionTransaction]:
        return self._transaction()

    async def commit(self) -> None:
        await self._session.commit()
