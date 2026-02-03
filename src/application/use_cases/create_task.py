from typing import ContextManager

from src.application.contracts.create_task import CreateTaskCommand, CreateTaskResult
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase
from src.domain.entities import Task


class FailedToCreateTask(UseCaseError):
    pass


class CreateTaskUseCase(IUseCase[CreateTaskCommand, CreateTaskResult]):
    def __init__(
        self, logger: ILogger, transaction_manager: ContextManager[ITransactionManager]
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    def execute(self, command: CreateTaskCommand) -> CreateTaskResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Creating new task")

        try:
            new_task = Task(payload=command.payload)

            with self._transaction_manager as tm:
                tm.tasks.save(new_task)
        except Exception as e:
            use_case_logger.exception("Failed to create new task")
            raise FailedToCreateTask from e

        use_case_logger.info(
            "Task created successfully", context={"new_task_id": new_task.id}
        )

        return CreateTaskResult(new_task_id=new_task.id)
