from __future__ import annotations
import datetime
from typing import List


class Currency:
    def __init__(
        self,
        name: str,
        rates: List[ConversionRate],
        last_update: datetime.datetime = None,
    ):
        self.name = name
        self.rates = rates
        self.last_update = last_update or datetime.datetime.now()


class ConversionRate:
    def __init__(self, code: str, rate: float):
        self.code = code
        self.rate = rate
