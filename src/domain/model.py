from __future__ import annotations
import datetime
from typing import List


class Analyses:
    def __init__(self, uuid: str, result: float):
        self.uuid = uuid
        self.result = result
