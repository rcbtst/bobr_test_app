from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

CommandType = TypeVar("CommandType", bound=BaseModel)
ResultType = TypeVar("ResultType", bound=BaseModel)


class IUseCase(Generic[CommandType, ResultType], ABC):
    def __call__(self, command: CommandType) -> ResultType:
        return self.execute(command)

    @abstractmethod
    def execute(self, command: CommandType) -> ResultType:
        pass
