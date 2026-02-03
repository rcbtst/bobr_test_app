from uuid import UUID

from src.application.contracts.base import Command, Result


class CreateTaskCommand(Command):
    payload: str


class CreateTaskResult(Result):
    new_task_id: UUID
