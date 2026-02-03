from celery import Celery, signals

from src.config import settings
from src.infrastructure.di_config import ApplicationContainer
from src.infrastructure.logging import configure_logging

configure_logging()

app = Celery("task_worker")

app.config_from_object("src.interfaces.workers.configs.task_worker")
app.conf.update(**settings.CELERY_TASK_WORKER_EXTRA_CONFIG)

app.autodiscover_tasks(packages=["src.interfaces.workers.tasks"], related_name=None)

app.conf.beat_schedule = {
    "enqueue_new_tasks_periodic": {
        "task": "enqueue_new_tasks",
        "schedule": settings.APP_PENDING_TASKS_SCHEDULE_INTERVAL,
    },
}

container = None


@signals.worker_process_init.connect
def init_worker(**kwargs: dict) -> None:
    global container
    container = ApplicationContainer()
    container.wire(
        packages=["src.interfaces.workers.tasks"],
    )
