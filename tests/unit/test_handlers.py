import pytest
from fastapi import HTTPException, status
from src.adapters import repository
from src.service_layer import unit_of_work
from src.domain import messages, model
from src import bootstrap


class FakeRepository(repository.AbstractRepository):
    def __init__(self, users):
        super().__init__()
        self._users = set(users)

    async def _add(self, users):
        self._users.add(users)

    async def _get(self, name=None, user_id=None):
        if name:
            return next((c for c in self._users if c.name == name), None)
        else:
            return next((c for c in self._users if c.id == user_id), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeRepository([])
        self.committed = False

    async def _commit(self):
        self.committed = True

    async def rollback(self):
        pass


class FakeEvent:
    pass


def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False,
        uow=FakeUnitOfWork(),
    )


class TestCreateUser:
    @pytest.fixture
    async def setup(self):
        bus = bootstrap_test_app()
        await bus.handle(messages.CreateUser(name='Dias'))
        return bus

    @pytest.mark.asyncio
    async def test_create_user(self, setup):
        bus = await setup
        assert (user := await bus.uow.users.get(name='Dias')) is not None
        assert len(user.transactions) == 0


class TestAddTransaction:
    @pytest.mark.asyncio
    async def test_add_transaction(self):
        bus = bootstrap_test_app()
        user = await bus.handle(messages.CreateUser(name='Dias'))

        transaction = await bus.handle(
            messages.AddTransaction(
                user_id=user.id,
                transaction_type=model.TransactionType.DEPOSIT.value,
                amount=100
            )
        )
        assert transaction is not None
        assert transaction.amount == 100
        assert transaction.transaction_type == model.TransactionType.DEPOSIT.value


class TestEvents:
    @pytest.mark.asyncio
    async def test_message_event(self):
        bus = bootstrap_test_app()
        try:
            await bus.handle(messages.CheckEvent())
        except Exception as e:
            pytest.fail('DID RAISE {0}'.format(e))

    @pytest.mark.asyncio
    async def test_message_unknown(self):
        bus = bootstrap_test_app()

        with pytest.raises(TypeError) as exc:
            await bus.handle(FakeEvent)
        assert isinstance(exc.value, TypeError)

