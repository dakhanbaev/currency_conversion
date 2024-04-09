import uvicorn
from fastapi import FastAPI, HTTPException, status
from src import bootstrap
from src.entrypoints import schemas, views
from src.domain import messages

bus = bootstrap.bootstrap()

app = FastAPI(root_path="/api/concurrency_conversion")


@app.get(
    "/update/{name}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResultSchema,
)
async def update_exchange_rates(name: str):
    cmd = messages.UpdateExchangeRates(name)
    await bus.handle(cmd)
    return schemas.ResultSchema(result="Updated successfully")


@app.get(
    "/last_update/{name}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.CurrencyGET,
)
async def last_update(name: str) -> schemas.CurrencyGET:
    result = await views.currencies(name, uow=bus.uow)
    if not result:
        raise HTTPException(status_code=404, detail="not found")
    return schemas.CurrencyGET(**result)


@app.post(
    "/convert",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResultSchema,
)
async def convert_currency(request: schemas.CurrencyConversionRequest):
    cmd = messages.ConvertCurrency(
        request.source_currency,
        request.target_currency,
        request.amount,
    )
    result = await bus.handle(cmd)
    return schemas.ResultSchema(result=result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
