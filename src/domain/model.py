from __future__ import annotations
import datetime
from typing import List
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class User:
    def __init__(
            self,
            name: str,
            transactions: List[Transaction],
            balances: List[Balance],
            created: datetime.datetime = None,
            balance: float = 0.0,
    ):
        self.name = name
        self.created = created or datetime.datetime.now()
        self.balance = balance
        self.balances = balances
        self.transactions = transactions


class Balance:
    def __init__(self, total: float, created: datetime.datetime = None):
        self.created = created or datetime.datetime.now()
        self.total = total


class Transaction:
    def __init__(self, transaction_type: str, amount: float, timestamp: datetime.datetime = None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = timestamp or datetime.datetime.now()
