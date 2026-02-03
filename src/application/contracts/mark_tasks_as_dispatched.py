from uuid import UUID

from src.application.contracts.base import Command


class MarkTasksAsDispatchedCommand(Command):
    task_ids: list[UUID]
