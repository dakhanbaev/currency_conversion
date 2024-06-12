# pylint: disable=redefined-outer-name
import pytest
from src import bootstrap
from src.entrypoints import views
from src.service_layer import unit_of_work
from src.domain import messages, model


@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=False,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
    )
    yield bus


@pytest.mark.asyncio
async def test_get_transaction(sqlite_bus):
    name = 'Dias'
    user = await sqlite_bus.handle(messages.CreateUser(name=name))
    transaction = await sqlite_bus.handle(messages.AddTransaction(
        user_id=user.id,
        transaction_type=model.TransactionType.DEPOSIT.value,
        amount=10.0
    ))

    result = await views.get_transaction(transaction.id, uow=sqlite_bus.uow)
    assert result
    assert result.get('amount', None)
    assert result['transaction_type'] == model.TransactionType.DEPOSIT.value
    assert result.get('timestamp', None)
