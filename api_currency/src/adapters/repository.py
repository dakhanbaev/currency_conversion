import abc
from typing import Set

from adapters import orm
from domain import model
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[model.Currency] = set()

    async def add(self, currency: model.Currency):
        await self._add(currency)
        self.seen.add(currency)

    async def get(self, name) -> model.Currency:
        if currency := await self._get(name):
            self.seen.add(currency)
        return currency

    @abc.abstractmethod
    async def _add(self, rates: model.Currency):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, name) -> model.Currency:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, currency_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_rate(self, currency_id: int, rate_code: str):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, currency: model.Currency):
        self.session.add(currency)

    async def _get(self, name: str) -> model.Currency:
        return (
            (await self.session.execute(select(model.Currency).filter_by(name=name)))
            .scalars()
            .one_or_none()
        )

    async def delete(self, currency_id: int):
        await self.session.execute(
            delete(model.ConversionRate).where(orm.conversion_rates.c.currency_id == currency_id)
        )

    async def get_rate(self, currency_id: int, rate_code: str) -> model.ConversionRate:
        return (
            (
                await self.session.execute(
                    select(model.ConversionRate).where(
                        and_(
                            orm.conversion_rates.c.currency_id == currency_id,
                            orm.conversion_rates.c.code == rate_code,
                        )
                    )
                )
            )
            .scalars()
            .one_or_none()
        )
