from uuid import UUID

from src.application.contracts.base import Command, Result
from src.domain.enums import TaskStatus


class ProcessTaskCommand(Command):
    task_id: UUID


class ProcessTaskResult(Result):
    result: str | None = None
    new_task_status: TaskStatus
