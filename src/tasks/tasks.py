from src.domain import messages
from src.celery_worker import celery_app


@celery_app
def save_analyse():
    pass


TASK_HANDLERS = {
    messages.SaveAnalyse: save_analyse,
}

