from src.service_layer import unit_of_work
from sqlalchemy.sql import text


async def get_analysis(request_id: str, frame: int,  uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        if frame:
            results = await uow.session.execute(
                text(
                    """
                    SELECT uuid, last_update, data, all_frame_count, frame 
                    FROM analyses
                    WHERE uuid = :request_id and frame = :frame
                    """
                ),
                {'request_id': request_id, 'frame': frame},
            )
        else:
            results = await uow.session.execute(
                text(
                    """
                    SELECT uuid, last_update, data, all_frame_count, frame 
                    FROM analyses
                    WHERE uuid = :request_id
                    """
                ),
                {'request_id': request_id},
            )

        return results.mappings().first()

