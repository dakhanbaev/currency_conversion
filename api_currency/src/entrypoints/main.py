import uvicorn
import logging
from fastapi import FastAPI, HTTPException, status
import bootstrap
from entrypoints import views
from entrypoints import schemas
from domain import messages

bus = bootstrap.bootstrap()

app = FastAPI(root_path="/api/concurrency_conversion")
logger = logging.getLogger(__name__)


@app.get(
    "/update/{name}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResultSchema,
)
async def update_exchange_rates(name: str):
    cmd = messages.UpdateExchangeRates(name)
    await bus.handle(cmd)
    logger.info(f"currency {name}: Updated successfully")
    return schemas.ResultSchema(result="Updated successfully")


@app.get(
    "/last_update/{name}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.CurrencyGET,
)
async def last_update(name: str) -> schemas.CurrencyGET:
    result = await views.currencies(name, uow=bus.uow)
    if not result:
        logger.error(f"Not result for currency: {name}")
        raise HTTPException(status_code=404, detail="not found")
    return schemas.CurrencyGET(**result)


@app.post(
    "/convert",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResultSchema,
)
async def convert_currency(convert: schemas.CurrencyConversionRequest):
    cmd = messages.ConvertCurrency(
        convert.source_currency,
        convert.target_currency,
        convert.amount,
    )
    result = await bus.handle(cmd)
    logger.info(
        f"Convert result for {convert.source_currency} -> "
        f"{convert.target_currency} : {result}"
    )
    return schemas.ResultSchema(result=result)


if __name__ == "__main__":
    # For debugging
    uvicorn.run(app, host="0.0.0.0", port=8000)
