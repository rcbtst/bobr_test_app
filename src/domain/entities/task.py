from datetime import datetime, UTC

from src.domain.entities.base import Entity
from src.domain.enums import TaskStatus

from pydantic import Field


class Task(Entity):
    payload: str
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    result: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    dispatched: bool = Field(default=False)
