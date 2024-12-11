# pylint: disable=redefined-outer-name
import pytest
from src import bootstrap
from src.entrypoints import views
from src.service_layer import unit_of_work
from src.domain import messages


@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=False,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
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
