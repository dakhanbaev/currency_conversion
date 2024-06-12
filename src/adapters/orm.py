import logging
from sqlalchemy import (
    Column,
    Float,
    String,
    Table,
    MetaData,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import registry, relationship

from src.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()
metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('created', DateTime(timezone=True)),
    Column('name', String(50), nullable=False, unique=True),
    Column('balance', Float, default=0.0, nullable=False),
)

balances = Table(
    'balances',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('created', DateTime(timezone=True)),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('total', Float, default=0.0, nullable=False),
)

transactions = Table(
    'transactions',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('transaction_type', String(20), nullable=False),
    Column('amount', Float, nullable=False),
    Column('timestamp', DateTime(timezone=True)),
)


def start_mappers():
    logger.info('Starting mappers')

    transactions_mapper = mapper_registry.map_imperatively(
        model.Transaction, transactions
    )

    balances_mapper = mapper_registry.map_imperatively(
        model.Balance, balances
    )

    mapper_registry.map_imperatively(
        model.User,
        users,
        properties={
            'transactions': relationship(transactions_mapper, lazy='selectin'),
            'balances': relationship(balances_mapper, lazy='selectin'),
        },
    )

