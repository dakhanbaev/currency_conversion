from typing import Union
from pydantic import BaseModel, UUID4


class Analysis(BaseModel):
    requestId: UUID4


class ResultSchema(BaseModel):
    result: Union[str, float]

