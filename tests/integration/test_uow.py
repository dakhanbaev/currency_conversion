import pytest
from sqlalchemy.sql import text

from src.service_layer import unit_of_work
from src.domain import model


async def get_currency(session, name):
    [[user_name]] = await session.execute(
        text(
            """
            SELECT name FROM users WHERE name = :name
            """
        ),
        {"name": name},
    )
    return user_name


async def insert_currency(session, name, balance):
    await session.execute(
        text("INSERT INTO users (name, balance) VALUES (:name, :balance)"),
        {"name": name, 'balance': balance},
    )


@pytest.mark.asyncio
async def test_uow_can_save_data(sqlite_session_factory):
    name = "Dias"
    session = sqlite_session_factory()
    await insert_currency(session, name, 10.0)
    await session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    async with uow:
        user = await uow.users.get(name=name)
        assert user.name == name
        new_user = model.User("Saken", [], [])
        await uow.users.add(new_user)
        await uow.commit()

    new_name = await get_currency(session, "Saken")
    assert new_name == "Saken"
