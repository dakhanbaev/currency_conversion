# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Union


class Command:
    pass


@dataclass
class CreateUser(Command):
    name: str


@dataclass
class AddTransaction(Command):
    user_id: int
    transaction_type: str
    amount: float


class Event:
    pass


@dataclass
class CheckEvent(Event):
    pass


Message = Union[Event, Command]
