from typing import Union, Any
from pydantic import BaseModel, UUID4
from datetime import datetime


class Analysis(BaseModel):
    uuid: str
    data: Any
    frame: int
    all_frame_count: int
    last_update: datetime


class ResultSchema(BaseModel):
    result: Union[str, float]

