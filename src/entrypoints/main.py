import uvicorn
import logging
from fastapi import FastAPI, HTTPException, status, UploadFile, File
from src import bootstrap
from src.entrypoints import schemas, views
from src.domain import messages

bus = bootstrap.bootstrap()

app = FastAPI(root_path='/api')
logger = logging.getLogger(__name__)


@app.delete(
    '/analysis/{request_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=schemas.Analysis,
)
async def delete_analysis(request_id: str):
    cmd = messages.DeleteAnalyse(request_id)
    await bus.handle(cmd)
    logger.info(f'currency {request_id}: Deleted successfully')
    return schemas.ResultSchema(result='Deleted successfully')


@app.get(
    '/analysis/{request_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Analysis,
)
async def get_analysis(request_id: str) -> schemas.CurrencyGET:
    result = await views.currencies(request_id, uow=bus.uow)
    if not result:
        logger.error(f'Not result for request_id : {request_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return schemas.CurrencyGET(**result)


@app.post(
    '/analysis',
    status_code=status.HTTP_201_CREATED,
)
async def post_analysis(file: UploadFile = File(...)):
    cmd = messages.SaveAnalyse(
        file
    )
    request_id = await bus.handle(cmd)
    return schemas.ResultSchema(result='OK')


if __name__ == '__main__':
    # For debugging
    uvicorn.run(app, host='0.0.0.0', port=8000)
