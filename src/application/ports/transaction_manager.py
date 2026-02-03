from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Optional, Type

from src.domain.repositories import ITaskRepository


class ITransactionManager(AbstractContextManager["ITransactionManager"], ABC):
    tasks: ITaskRepository

    @abstractmethod
    def __enter__(self) -> ITransactionManager:
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        pass
