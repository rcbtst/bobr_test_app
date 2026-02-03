from typing import ContextManager

from src.application.contracts.get_task import GetTaskCommand, GetTaskResult
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase


class TaskNotFound(UseCaseError):
    pass


class FailedToGetTask(UseCaseError):
    pass


class GetTaskUseCase(IUseCase[GetTaskCommand, GetTaskResult]):
    def __init__(
        self, logger: ILogger, transaction_manager: ContextManager[ITransactionManager]
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    def execute(self, command: GetTaskCommand) -> GetTaskResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Getting task")

        try:
            with self._transaction_manager as tm:
                task = tm.tasks.get_by_id(command.task_id)
                if task is None:
                    use_case_logger.error("Task not found")
                    raise TaskNotFound

        except TaskNotFound:
            raise
        except Exception as e:
            use_case_logger.exception("Failed to get task")
            raise FailedToGetTask from e

        use_case_logger.info("Task retrieved successfully")

        return GetTaskResult(result=task.result, status=task.status)
