from typing import Union
from pydantic import BaseModel, field_validator
from datetime import datetime


class ResultSchema(BaseModel):
    result: Union[str, float]


class RateSchema(BaseModel):
    code: str
    rate: float


class CurrencyGET(BaseModel):
    name: str
    last_update: datetime


class CurrencyConversionRequest(BaseModel):
    source_currency: str
    target_currency: str
    amount: float

    @classmethod
    @field_validator("source_currency")
    def validate_source_currency(cls, source_currency):
        if source_currency is None or source_currency == "":
            raise ValueError("source_currency cannot be None or empty")
        return source_currency

    @classmethod
    @field_validator("target_currency")
    def validate_target_currency(cls, target_currency):
        if target_currency is None or target_currency == "":
            raise ValueError("target_currency cannot be None or empty")
        return target_currency

    @classmethod
    @field_validator("amount")
    def validate_amount(cls, amount):
        if amount is None or amount <= 0:
            raise ValueError("amount cannot be None or amount <= 0")
        return amount
