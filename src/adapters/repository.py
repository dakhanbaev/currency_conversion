import abc
from typing import Set

from src.domain import model
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[model.Analyses] = set()

    async def add(self, analyses: model.Analyses):
        await self._add(analyses)
        self.seen.add(analyses)

    async def get(self, uuid: str) -> model.Analyses:
        if analyses := await self._get(uuid):
            self.seen.add(analyses)
        return analyses

    @abc.abstractmethod
    async def _add(self, rates: model.Analyses):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, uuid: str) -> model.Analyses:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, uuid: str):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, analyses: model.Analyses):
        self.session.add(analyses)

    async def _get(self, uuid: str) -> model.Analyses:
        return (
            (await self.session.execute(select(model.Analyses).filter_by(uuid=uuid)))
            .scalars()
            .one_or_none()
        )

    async def delete(self, uuid: str):
        await self.session.execute(
            delete(model.Analyses).filter_by(uuid=uuid)
        )

