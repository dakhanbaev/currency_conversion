# pylint: disable=broad-except, attribute-defined-outside-init
from __future__ import annotations
import functools
import logging
from typing import TYPE_CHECKING, Callable, Dict, List, Type, Iterable

from fastapi import HTTPException, status
from src.domain import messages

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[messages.Event], List[Callable]],
        command_handlers: Dict[Type[messages.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue = []

    async def handle(self, message: messages.Message):
        self.queue = [message]
        results = []
        while self.queue:
            message = self.queue.pop(0)
            result = await self._handle(message)
            if not isinstance(result, Iterable) or isinstance(result, str):
                result = [result]

            results.extend(v for v in result if v is not None)

        if results:
            return results[0]

    @functools.singledispatchmethod
    def _handle(self, message: messages.Message):
        raise TypeError(f"Unknown message. {type(message)}")

    @_handle.register(messages.Event)
    async def _(self, event: messages.Event):
        results = []
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                if result := await handler(event):
                    results.append(result)
                self.queue.extend(self.uow.collect_new_events())
                return results
            except Exception as e:
                logger.exception("Exception handling event %s", event)
                logger.exception(e)
                continue

    @_handle.register(messages.Command)
    async def _(self, command: messages.Command):
        results = []
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            if result := await handler(command):
                results.append(result)
            self.queue.extend(self.uow.collect_new_events())
            return results
        except Exception as e:
            logger.exception("Exception handling command %s", command)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
