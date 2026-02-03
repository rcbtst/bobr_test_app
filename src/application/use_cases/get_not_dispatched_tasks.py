from typing import ContextManager

from src.application.contracts.get_not_dispatched_tasks import (
    GetNotDispatchedTasksCommand,
    GetNotDispatchedTasksResult,
)
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase


class FailedToGetNotDispatchedTasks(UseCaseError):
    pass


class GetNotDispatchedTasksUseCase(
    IUseCase[GetNotDispatchedTasksCommand, GetNotDispatchedTasksResult]
):
    def __init__(
        self, logger: ILogger, transaction_manager: ContextManager[ITransactionManager]
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    def execute(
        self, command: GetNotDispatchedTasksCommand
    ) -> GetNotDispatchedTasksResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Getting not dispatched tasks")

        try:
            with self._transaction_manager as tm:
                not_dispatched_task_ids = tm.tasks.get_all_not_dispatched_ids(
                    limit=command.limit
                )
        except Exception as e:
            use_case_logger.exception("Failed to get not dispatched tasks")
            raise FailedToGetNotDispatchedTasks from e

        use_case_logger.info(
            "Not dispatched tasks fetched successfully",
            context={"total_tasks_qty_fetched": len(not_dispatched_task_ids)},
        )

        return GetNotDispatchedTasksResult(
            not_dispatched_task_ids=not_dispatched_task_ids
        )
