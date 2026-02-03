from typing import ContextManager

from src.application.contracts.base import NoneResult
from src.application.contracts.mark_tasks_as_dispatched import (
    MarkTasksAsDispatchedCommand,
)
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase


class FailedToMarkTasksAsDispatched(UseCaseError):
    pass


class MarkTasksAsDispatchedUseCase(IUseCase[MarkTasksAsDispatchedCommand, NoneResult]):
    def __init__(
        self, logger: ILogger, transaction_manager: ContextManager[ITransactionManager]
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    def execute(self, command: MarkTasksAsDispatchedCommand) -> NoneResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Marking tasks as dispatched")

        try:
            with self._transaction_manager as tm:
                tm.tasks.mark_as_dispatched(command.task_ids)
        except Exception as e:
            use_case_logger.exception("Failed to mark tasks as dispatched")
            raise FailedToMarkTasksAsDispatched from e

        use_case_logger.info("Tasks marked as dispatched successfully")

        return NoneResult()
