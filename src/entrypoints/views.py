from src.service_layer import unit_of_work
from sqlalchemy.sql import text
from datetime import datetime


async def get_balance(user_id: int, timestamp: datetime, uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        results = await uow.session.execute(
            text(
                """
                SELECT total, created, user_id FROM balances 
                WHERE user_id = :user_id and date_trunc('second', created) = :timestamp
                """
            ),
            {'user_id': user_id, 'timestamp': timestamp},
        )
        return results.mappings().first()


async def get_transaction(transaction_id: int, uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        results = await uow.session.execute(
            text(
                """
                SELECT id, user_id, transaction_type, amount, timestamp FROM transactions WHERE id = :transaction_id
                """
            ),
            {'transaction_id': transaction_id},
        )
        return results.mappings().first()

