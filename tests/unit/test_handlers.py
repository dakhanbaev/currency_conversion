import pytest
from src.adapters import repository
from src.service_layer import unit_of_work
from src.external_service import external_api
from src.domain import messages
from src import bootstrap


class FakeRepository(repository.AbstractRepository):
    def __init__(self, currencies):
        super().__init__()
        self._currencies = set(currencies)

    async def _add(self, currencies):
        self._currencies.add(currencies)

    async def _get(self, name):
        return next((c for c in self._currencies if c.name == name), None)

    async def delete(self, currency_id: int):
        pass

    async def get_rate(self, currency_id: int, rate_code: str):
        return next(
            (
                r
                for c in self._currencies
                for r in c.rates
                if (r.code == rate_code and c.id == currency_id)
            ),
            None,
        )


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.currencies = FakeRepository([])
        self.committed = False

    async def _commit(self):
        self.committed = True

    async def rollback(self):
        pass


class FakeExchangeRateApi(external_api.ExternalApi):
    async def get_all_rates(self, code: str):
        return {
            "USD": 1,
            "AED": 3.6725,
            "AFN": 73.7913,
            "ALL": 95.7917,
            "AMD": 405.2462,
        }


def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False, uow=FakeUnitOfWork(), api=FakeExchangeRateApi()
    )


class TestUpdateExchangeRates:
    @pytest.mark.asyncio
    async def test_update_rate(self):
        bus = bootstrap_test_app()
        await bus.handle(messages.UpdateExchangeRates(name="BTS"))
        assert (currency2 := await bus.uow.currencies.get("BTS")) is not None
        assert len(currency2.rates) == 5


class TestConvertCurrency:
    @pytest.mark.asyncio
    async def test_convert_currency(self):
        bus = bootstrap_test_app()
        result = await bus.handle(
            messages.ConvertCurrency(
                source_currency="BTS", target_currency="USD", amount=100
            )
        )
        assert result is not None
        assert result == 100
