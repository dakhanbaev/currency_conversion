# pylint: disable=redefined-outer-name
import pytest
import bootstrap
from entrypoints import views
from service_layer import unit_of_work
from external_service import external_api
from domain import messages


class FakeExchangeRateApi(external_api.ExternalApi):
    async def get_all_rates(self, code: str):
        return {
            "USD": 1,
            "AED": 3.6725,
            "AFN": 73.7913,
            "ALL": 95.7917,
            "AMD": 405.2462,
        }


@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=False,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
        api=FakeExchangeRateApi(),
    )
    yield bus


@pytest.mark.asyncio
async def test_currencies_view(sqlite_bus):
    name = "BTS"
    await sqlite_bus.handle(messages.UpdateExchangeRates(name=name))

    result = await views.currencies(name, uow=sqlite_bus.uow)
    assert result
    assert result.get("name", None)
    assert result["name"] == name
    assert result.get("last_update", None)
