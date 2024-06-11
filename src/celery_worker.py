from celery import Celery
from src.config import get_redis_uri


celery_app = Celery('tasks', broker=get_redis_uri(), backend=get_redis_uri())

