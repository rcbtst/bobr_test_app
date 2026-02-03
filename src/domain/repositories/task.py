from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.task import Task
from src.domain.repositories.base import IRepository


class ITaskRepository(IRepository[Task], ABC):
    @abstractmethod
    def mark_as_dispatched(self, task_ids: list[UUID]) -> None:
        pass

    @abstractmethod
    def get_all_not_dispatched_ids(self, limit: int | None = None) -> list[UUID]:
        pass
