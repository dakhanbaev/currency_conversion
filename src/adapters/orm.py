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
    ARRAY
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
    Column('uuid', String(100)),
    Column('frame', Integer),
    Column('all_frame_count', Integer),
    Column('data', ARRAY(Float)),
    Column('last_update', DateTime(timezone=True)),
)


def start_mappers():
    logger.info('Starting mappers')

    mapper_registry.map_imperatively(
        model.Analyses, analyses
    )

