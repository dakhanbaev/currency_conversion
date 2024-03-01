import pytest
from src.adapters import repository
from src.domain import model


class TestSqlAlchemyRepository:
    @pytest.fixture
    async def setup(self, session):
        repo = repository.SqlAlchemyRepository(session)
        rate1 = model.ConversionRate(code="USD", rate=10.5)
        rate2 = model.ConversionRate(code="EUR", rate=20.8)
        currency = model.Currency(name="USD", rates=[rate1, rate2])
        await repo.add(currency)
        return repo, currency

    @pytest.mark.asyncio
    async def test_get_rate(self, setup):
        repo, currency = await setup

        currency = await repo.get("USD")
        result = await repo.get_rate(currency_id=currency.id, rate_code="USD")
        result2 = await repo.get_rate(currency_id=currency.id, rate_code="EUR")

        assert result == currency.rates[0]
        assert result2 == currency.rates[1]

    @pytest.mark.asyncio
    async def test_delete(self, setup):
        repo, currency = await setup
        currency = await repo.get("USD")

        await repo.delete(currency_id=currency.id)
        await repo.session.commit()
        result = await repo.get_rate(currency_id=currency.id, rate_code="USD")
        result2 = await repo.get_rate(currency_id=currency.id, rate_code="EUR")

        repo.session.expunge_all()

        cur = await repo.get("USD")
        assert cur.rates == []
        assert result is None
        assert result2 is None
