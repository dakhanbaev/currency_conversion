import uvicorn
import logging
from fastapi import FastAPI, HTTPException, status
from src import bootstrap
from src.entrypoints import schemas, views
from src.domain import messages

bus = bootstrap.bootstrap()

app = FastAPI(root_path='/api/v1')
logger = logging.getLogger(__name__)


@app.post(
    '/user',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.GETUser,
)
async def create_user(user: schemas.POSTUser):
    cmd = messages.CreateUser(user.name)
    new_user = await bus.handle(cmd)
    logger.info(
        f'Create user with name: {user.name} , user_id: {new_user.id}'
        )
    return new_user


@app.patch(
    '/user/{user_id}/balance',
    status_code=status.HTTP_200_OK,
    response_model=schemas.BalanceResult,
)
async def get_user_balance(user_id: int, balance: schemas.GETBalanceTimestamp):
    result = await views.get_balance(user_id, balance.timestamp, uow=bus.uow)
    if not result:
        logger.error(f'Not result for user: {user_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return result


@app.post(
    '/transaction',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.GETTransaction,
)
async def add_transaction(transaction: schemas.POSTTransaction) -> schemas.GETTransaction:

    cmd = messages.AddTransaction(
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
    )
    new_transaction = await bus.handle(cmd)
    logger.info(
        f'Create transaction for user : {transaction.user_id}'
        f'transaction_type: {transaction.transaction_type}'
        f'amount: {transaction.amount}'
    )
    return new_transaction


@app.get(
    '/transaction/{transaction_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.GETTransaction,
)
async def incoming_transaction(transaction_id: int):
    transaction = await views.get_transaction(transaction_id, uow=bus.uow)
    if not transaction:
        logger.error(f'Not transaction for transaction_id: {transaction_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return transaction


if __name__ == '__main__':
    # For debugging
    uvicorn.run(app, host='0.0.0.0', port=8001)
