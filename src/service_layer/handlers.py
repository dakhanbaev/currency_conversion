# pylint: disable=unused-argument
from __future__ import annotations

from typing import TYPE_CHECKING

from src.domain import messages


if TYPE_CHECKING:

    import unit_of_work


class InvalidCode(Exception):
    pass


async def delete_analyse(
    analyse: messages.DeleteAnalyse,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    async with uow:
        await uow.analyses.delete(uuid=analyse.request_id)
        await uow.commit()


async def check_events(check: messages.CheckEvent):
    pass


COMMAND_HANDLERS = {
    messages.DeleteAnalyse: delete_analyse,
}

EVENT_HANDLERS = {messages.CheckEvent: [check_events]}
