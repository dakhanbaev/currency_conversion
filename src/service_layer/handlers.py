# pylint: disable=unused-argument
from __future__ import annotations

from typing import TYPE_CHECKING

from src.domain import messages
from src.celery_app import analyze_content


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


def analyze_content_handler(
    analyse: messages.SaveAnalyse,
):
    analyze_content.delay(analyse.__dict__)


TASK_HANDLERS = {
    messages.SaveAnalyse: analyze_content_handler,
}


COMMAND_HANDLERS = {
    messages.DeleteAnalyse: delete_analyse,
}

EVENT_HANDLERS = {messages.CheckEvent: [check_events]}
