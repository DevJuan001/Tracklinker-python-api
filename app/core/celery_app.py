from celery import Celery

from app.core.config import settings

celery = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email_tasks"]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Bogota",
    enable_utc=True,
)
