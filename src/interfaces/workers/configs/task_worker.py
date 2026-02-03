from sqlalchemy.engine import URL

from src.config import settings

DATABASE_URL = URL.create(
    drivername=settings.DB_DRIVER,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD.get_secret_value(),
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
).render_as_string(hide_password=False)

task_acks_late = True
task_acks_on_failure_or_timeout = False
task_reject_on_worker_lost = True
task_time_limit = 60 * 5
worker_max_tasks_per_child = 50
worker_prefetch_multiplier = 1
worker_hijack_root_logger = False
worker_proc_alive_timeout = 120
result_backend = f"db+{DATABASE_URL}"
result_extended = True
result_expires = 60 * 60 * 24 * 14
database_create_tables_at_setup = False
broker_url = settings.CELERY_BROKER_URL
task_serializer = "json"
accept_content = ["json"]
