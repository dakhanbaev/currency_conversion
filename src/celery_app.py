from celery import Celery
from src.config import get_redis_uri
from src.tasks. task_handlers import AnalyzeContent


celery_app = Celery(
    'worker',
    broker=get_redis_uri(),
    backend=get_redis_uri(),
    include=['src.tasks']
)

analyze_content = celery_app.register_task(AnalyzeContent())
celery_app.autodiscover_tasks()

