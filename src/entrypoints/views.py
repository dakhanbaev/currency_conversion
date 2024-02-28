from src.service_layer import unit_of_work
from sqlalchemy.sql import text


async def currencies(name: str, uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        results = await uow.session.execute(
            text(
                """
                SELECT name, last_update FROM currencies WHERE name = :name
                """
            ),
            {"name": name},
        )
        return results.mappings().first()

