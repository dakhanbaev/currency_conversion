# pylint: disable=unused-argument
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from src.domain import messages, model
from src.external_service import external_api


if TYPE_CHECKING:

    import unit_of_work


class InvalidCode(Exception):
    pass


async def update_rate(
    currency_name: messages.UpdateExchangeRates,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    api: external_api.ExchangeRateApi,
):
    async with uow:
        if (currency := await uow.currencies.get(name=currency_name.name)) is None:
            currency = model.Currency(
                name=currency_name.name,
                rates=[],
            )
            await uow.currencies.add(currency)
        else:
            await uow.currencies.delete(currency_id=currency.id)
        rates = await api.get_all_rates(code=currency_name.name)
        currency.rates.extend(
            [model.ConversionRate(code=code, rate=rate) for code, rate in rates.items()]
        )
        currency.last_update = datetime.datetime.now()
        await uow.commit()


async def convert_currency(
    convert: messages.ConvertCurrency,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    api: external_api.ExchangeRateApi,
) -> float:
    async with uow:
        if (currency := await uow.currencies.get(name=convert.source_currency)) is None:
            await update_rate(
                messages.UpdateExchangeRates(name=convert.source_currency),
                uow=uow,
                api=api,
            )
            currency = await uow.currencies.get(name=convert.source_currency)
        conversion_rate = await uow.currencies.get_rate(
            currency_id=currency.id, rate_code=convert.target_currency
        )
        return convert.amount * conversion_rate.rate


async def check_events(check: messages.CheckEvent):
    pass


COMMAND_HANDLERS = {
    messages.UpdateExchangeRates: update_rate,
    messages.ConvertCurrency: convert_currency,
}

EVENT_HANDLERS = {messages.CheckEvent: [check_events]}
