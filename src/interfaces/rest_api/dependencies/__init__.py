from src.interfaces.rest_api.dependencies.logger import LoggerDep
from src.interfaces.rest_api.dependencies.use_cases import (
    CreateTaskUseCaseDep,
    GetTaskUseCaseDep,
)

__all__ = [
    "CreateTaskUseCaseDep",
    "GetTaskUseCaseDep",
    "LoggerDep",
]
