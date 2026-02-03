from uuid import UUID

from pydantic import Field

from src.application.contracts.base import Command, Result


class GetNotDispatchedTasksCommand(Command):
    limit: int | None = Field(default=50, gt=0)


class GetNotDispatchedTasksResult(Result):
    not_dispatched_task_ids: list[UUID] = Field(default_factory=list)
