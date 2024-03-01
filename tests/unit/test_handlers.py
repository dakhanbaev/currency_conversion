import pytest
from fastapi import HTTPException, status
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
        for c in self._currencies:
            if c.id == currency_id:
                del c.rates

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


class FakeEvent:
    pass


def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False, uow=FakeUnitOfWork(), api=FakeExchangeRateApi()
    )


class TestUpdateExchangeRates:
    @pytest.fixture
    async def setup(self):
        bus = bootstrap_test_app()
        await bus.handle(messages.UpdateExchangeRates(name="BTS"))
        return bus

    @pytest.mark.asyncio
    async def test_update_rate(self, setup):
        bus = await setup
        assert (currency2 := await bus.uow.currencies.get("BTS")) is not None
        assert len(currency2.rates) == 5

    @pytest.mark.asyncio
    async def test_update_rate_with_exits_currency(self, setup):
        bus = await setup
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

    @pytest.mark.asyncio
    async def test_convert_currency_with_not_exits_rate(self):
        bus = bootstrap_test_app()

        with pytest.raises(HTTPException) as exc:
            await bus.handle(
                messages.ConvertCurrency(
                    source_currency="BTS", target_currency="BTS", amount=100
                )
            )
        assert isinstance(exc.value, HTTPException)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestEvents:
    @pytest.mark.asyncio
    async def test_message_event(self):
        bus = bootstrap_test_app()
        try:
            await bus.handle(messages.CheckEvent())
        except Exception as e:
            pytest.fail("DID RAISE {0}".format(e))

    @pytest.mark.asyncio
    async def test_message_unknown(self):
        bus = bootstrap_test_app()

        with pytest.raises(TypeError) as exc:
            await bus.handle(FakeEvent)
        assert isinstance(exc.value, TypeError)
        assert exc.value.args == ("Unknown message. <class 'type'>",)
