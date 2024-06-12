from typing import Union, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime


class POSTUser(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name):
        if name is None or name == "":
            raise ValueError("name cannot be None or empty")
        return name


class GETUser(BaseModel):
    id: int
    name: str
    balance: float


class GETBalanceTimestamp(BaseModel):
    timestamp: Optional[datetime]


class BalanceResult(BaseModel):
    user_id: int
    total: float
    created: datetime


class POSTTransaction(BaseModel):
    user_id: int
    transaction_type: str
    amount: float

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, user_id):
        if user_id is None:
            raise ValueError("user_id cannot be None")
        return user_id

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, amount):
        if amount is None or amount <= 0:
            raise ValueError("amount cannot be None or amount <= 0")
        return amount

    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, transaction_type):
        if transaction_type is None or transaction_type == "":
            raise ValueError("transaction_type cannot be None or empty")
        return transaction_type


class GETTransaction(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    timestamp: datetime


class ResultSchema(BaseModel):
    result: Union[str, int]


