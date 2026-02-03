from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        nested_model_default_partial_update=True,
    )

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_DRIVER: str = "postgresql+psycopg2"

    CELERY_BROKER_URL: str
    CELERY_TASK_WORKER_EXTRA_CONFIG: dict[str, object] = Field(default_factory=dict)

    APP_PENDING_TASKS_SCHEDULE_INTERVAL: int = Field(default=10, gt=0)
    APP_MAX_PENDING_TASKS_TO_ENQUEUE_AT_ONCE: int = Field(default=50, gt=0)


settings = EnvSettings()
