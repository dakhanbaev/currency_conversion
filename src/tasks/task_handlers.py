import datetime
import asyncio

from sqlalchemy.exc import ArgumentError
from celery import Task
from celery.utils.log import get_task_logger
from src.domain import model
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.services import analysis_service
from src.adapters import orm

logger = get_task_logger(__name__)


class AnalyzeContent(Task):
    date: str
    service_analysis: analysis_service.AnalysisService = analysis_service.AnalysisService()
    uow: SqlAlchemyUnitOfWork = SqlAlchemyUnitOfWork()

    @property
    def general_log(self):
        return f"{self.__class__.__name__} {self.date}"

    def run(
            self,
            analyse: dict,
    ):
        self.date = datetime.datetime.now().strftime('%d-%m-%Y')
        loop = asyncio.get_event_loop()
        logger.info(f'{self.general_log} STARTED')
        try:
            orm.start_mappers()
        except ArgumentError:
            pass
        loop.run_until_complete(self.analyze_content_and_save(
            analyse['request_id'],
            analyse['file_path'],
            analyse['file_content_type'],
            self.uow
        ))
        logger.info(f'{self.general_log} FINISHED')

    async def analyze_content_and_save(self, request_id: str, file_path, content_type, uow: SqlAlchemyUnitOfWork):
        async with uow:
            result = self.service_analysis.analyze(file_path, content_type)
            for i, data in enumerate(result):
                analyses = model.Analyses(
                    uuid=request_id,
                    frame=i,
                    all_frame_count=len(result),
                    data=data
                )
                await uow.analyses.add(analyses)
            await uow.commit()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info(f'Task {task_id}| {self.general_log} failed: {exc}')


