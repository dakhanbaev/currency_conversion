import abc
from typing import Set

from src.domain import model
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[model.User] = set()

    async def add(self, user: model.User):
        await self._add(user)
        self.seen.add(user)

    async def get(self, name: str = None, user_id: int = None) -> model.User:
        if user := await self._get(name, user_id):
            self.seen.add(user)
        return user

    @abc.abstractmethod
    async def _add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, name: str, user_id: int) -> model.User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, user: model.User):
        self.session.add(user)

    async def _get(self, name: str = None, user_id: int = None) -> model.User:
        if name:
            return (
                (await self.session.execute(select(model.User).filter_by(name=name)))
                .scalars()
                .one_or_none()
            )
        else:
            return (
                (await self.session.execute(select(model.User).filter_by(id=user_id)))
                .scalars()
                .one_or_none()
            )

