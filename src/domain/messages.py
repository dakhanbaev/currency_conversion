# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Union


class Command:
    pass


@dataclass
class UpdateExchangeRates(Command):
    name: str


@dataclass
class ConvertCurrency(Command):
    source_currency: str
    target_currency: str
    amount: float


class Event:
    pass


Message = Union[Event, Command]

