from uuid import UUID

from src.application.contracts.base import Command, Result
from src.domain.enums import TaskStatus


class GetTaskCommand(Command):
    task_id: UUID


class GetTaskResult(Result):
    result: str | None = None
    status: TaskStatus
