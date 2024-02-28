import pytest
from src.adapters import repository
from src.domain import model


@pytest.mark.asyncio
async def test_get_rate(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyRepository(session)
    rate1 = model.ConversionRate(code="USD", rate=10.5)
    rate2 = model.ConversionRate(code="EUR", rate=20.8)
    currency = model.Currency(name="USD", rates=[rate1, rate2])
    await repo.add(currency)
    currency = await repo.get("USD")
    result = await repo.get_rate(currency_id=currency.id, rate_code="USD")
    assert result == rate1
