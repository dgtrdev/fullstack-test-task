import asyncio

from celery import Celery

from src.services import processing
from src.settings import settings


_worker_loop: asyncio.AbstractEventLoop | None = None
celery_app = Celery("file_tasks", broker=settings.redis_url, backend=settings.redis_url)


def run_in_worker_loop(coroutine):
    global _worker_loop
    if _worker_loop is None or _worker_loop.is_closed():
        _worker_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_worker_loop)
    return _worker_loop.run_until_complete(coroutine)


@celery_app.task
def scan_file_for_threats(file_id: str) -> None:
    run_in_worker_loop(processing.check_file_safety(file_id))
    extract_file_metadata.delay(file_id)


@celery_app.task
def extract_file_metadata(file_id: str) -> None:
    run_in_worker_loop(processing.get_file_metadata(file_id))
    send_file_alert.delay(file_id)


@celery_app.task
def send_file_alert(file_id: str) -> None:
    run_in_worker_loop(processing.create_processing_alert(file_id))
