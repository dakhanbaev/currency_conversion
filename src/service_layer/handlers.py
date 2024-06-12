# pylint: disable=unused-argument
from __future__ import annotations

from typing import TYPE_CHECKING

from src.domain import messages, model


if TYPE_CHECKING:

    import unit_of_work


async def create_user(
    user_name: messages.CreateUser,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
) -> model.User:
    async with uow:
        if (user := await uow.users.get(name=user_name.name)) is None:
            user = model.User(
                name=user_name.name,
                transactions=[],
                balances=[],
            )
            await uow.users.add(user)
        await uow.commit()
        return user


async def add_transaction(
    transaction: messages.AddTransaction,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
) -> model.Transaction:
    async with uow:
        if (user := await uow.users.get(user_id=transaction.user_id)) is None:
            raise Exception(f'No user with id : {transaction.user_id}')

        if transaction.transaction_type == model.TransactionType.WITHDRAW.value:
            if (total_balance := user.balance - transaction.amount) < 0:
                raise Exception(f'Can not create transaction with this amount : {transaction.amount}')
        elif transaction.transaction_type == model.TransactionType.DEPOSIT.value:
            total_balance = user.balance + transaction.amount
        else:
            raise Exception(f'Unexpected transaction type : {transaction.transaction_type}')

        user.balance = total_balance
        new_transaction = model.Transaction(
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
            )
        balance = model.Balance(
            total=total_balance
        )

        user.transactions.append(new_transaction)
        user.balances.append(balance)

        await uow.commit()
        return new_transaction


async def check_events(check: messages.CheckEvent):
    pass


COMMAND_HANDLERS = {
    messages.CreateUser: create_user,
    messages.AddTransaction: add_transaction,
}

EVENT_HANDLERS = {messages.CheckEvent: [check_events]}
