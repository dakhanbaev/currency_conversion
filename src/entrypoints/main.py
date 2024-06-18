import uvicorn
import logging
from typing import Optional
import uuid
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
)
async def delete_analysis(request_id: str):
    cmd = messages.DeleteAnalyse(request_id)
    await bus.handle(cmd)
    logger.info(f'analysis {request_id}: Deleted successfully')


@app.get(
    '/analysis/{request_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Analysis,
)
async def get_analysis(request_id: str, frame: Optional[int] = None) -> schemas.Analysis:
    result = await views.get_analysis(request_id, frame,  uow=bus.uow)
    if not result:
        logger.error(f'Not result for request_id : {request_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return result


@app.get(
    '/analysis/{request_id}/{frame}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Analysis,
)
async def get_analysis(request_id: str, frame: Optional[int] = None) -> schemas.Analysis:
    result = await views.get_analysis(request_id, frame,  uow=bus.uow)
    if not result:
        logger.error(f'Not result for request_id : {request_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return result


@app.post(
    '/analysis',
    status_code=status.HTTP_201_CREATED,
)
async def post_analysis(file: UploadFile = File(...)):
    import os
    request_id = str(uuid.uuid4())
    _, file_extension = os.path.splitext(file.filename)
    unique_filename = f"{request_id}{file_extension}"
    file_path = os.path.join("src/uploads", unique_filename)

    with open(file_path, "wb") as video_file:
        video_file.write(await file.read())

    cmd = messages.SaveAnalyse(
        request_id,
        file_path,
        file.content_type
    )
    await bus.handle(cmd)
    return schemas.ResultSchema(result=request_id)


if __name__ == '__main__':
    # For debugging
    uvicorn.run(app, host='0.0.0.0', port=8012)
