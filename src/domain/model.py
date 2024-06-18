from __future__ import annotations
import datetime
from typing import Any


class Analyses:
    def __init__(
            self,
            uuid: str,
            data: list,
            frame: int,
            all_frame_count: int,
            last_update: datetime = datetime.datetime.now()
    ):
        self.uuid = uuid
        self.data = data
        self.frame = frame
        self.all_frame_count = all_frame_count
        self.last_update = last_update or datetime.datetime.now()


