import pytest
from sqlalchemy.sql import text

from src.service_layer import unit_of_work
from src.domain import model


async def get_currency(session, name):
    [[currency_name]] = await session.execute(
        text(
            """
            SELECT name FROM currencies WHERE name = :name
            """
        ),
        {"name": name},
    )
    return currency_name


async def insert_currency(session, name):
    await session.execute(
        text("INSERT INTO currencies (name) VALUES (:name)"),
        {"name": name},
    )


@pytest.mark.asyncio
async def test_uow_can_save_data(sqlite_session_factory):
    code = "KZT"
    session = sqlite_session_factory()
    await insert_currency(session, code)
    await session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    async with uow:
        currency = await uow.currencies.get(name=code)
        assert currency.name == code
        new_currency = model.Currency("RUB", [])
        await uow.currencies.add(new_currency)
        await uow.commit()

    new_code = await get_currency(session, "RUB")
    assert new_code == "RUB"

