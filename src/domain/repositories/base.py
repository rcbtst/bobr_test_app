from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class IRepository(Generic[T], ABC):
    @abstractmethod
    def save(self, obj: T) -> None:
        """Persist/update entity"""
        pass

    @abstractmethod
    def get_by_id(self, obj_id: UUID) -> T | None:
        """Load entity by its ID, or return None if it's not found"""
        pass
