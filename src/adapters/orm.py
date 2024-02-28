import logging
from sqlalchemy import Column, Float, String, Table, MetaData, Integer, ForeignKey, DateTime
from sqlalchemy.orm import registry, relationship

from src.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()
metadata = MetaData()

currencies = Table(
    "currencies",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(10), unique=True),
    Column("last_update", DateTime(timezone=True))
)

conversion_rates = Table(
    "conversion_rates",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", String(10)),
    Column("currency_id", ForeignKey("currencies.id")),
    Column("rate", Float),
)


def start_mappers():
    logger.info("Starting mappers")

    conversion_rates_mapper = mapper_registry.map_imperatively(
        model.ConversionRate,
        conversion_rates
    )

    mapper_registry.map_imperatively(
        model.Currency,
        currencies,
        properties={"rates": relationship(conversion_rates_mapper, lazy="selectin")}
    )


