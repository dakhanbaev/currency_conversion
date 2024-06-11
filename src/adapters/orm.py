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
from sqlalchemy.orm import registry

from src.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()
metadata = MetaData()

analyses = Table(
    'analyses',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uuid', String(10), unique=True),
    Column('last_update', DateTime(timezone=True)),
)


def start_mappers():
    logger.info('Starting mappers')

    conversion_rates_mapper = mapper_registry.map_imperatively(
        model.ConversionRate, analyses
    )

