import pytest
from src.adapters import repository
from src.domain import model


class TestSqlAlchemyRepository:
    @pytest.fixture
    async def setup(self, session):
        repo = repository.SqlAlchemyRepository(session)
        transaction1 = model.Transaction(transaction_type=model.TransactionType.DEPOSIT.value, amount=10.5)
        transaction2 = model.Transaction(transaction_type=model.TransactionType.WITHDRAW.value, amount=20.5)
        user = model.User(name='Dias', transactions=[transaction1, transaction2], balances=[])
        await repo.add(user)
        return repo, user

    @pytest.mark.asyncio
    async def test_get_user(self, setup):
        repo, new_user = await setup

        user = await repo.get('Dias')

        assert user == new_user
        assert len(user.transactions) == 2

