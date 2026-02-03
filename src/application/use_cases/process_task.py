from random import randint
from time import sleep
from typing import ContextManager

from src.application.contracts.process_task import ProcessTaskCommand, ProcessTaskResult
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase
from src.domain.entities import Task
from src.domain.enums import TaskStatus


class TaskToProcessNotFound(UseCaseError):
    pass


class TaskAlreadyProcessed(UseCaseError):
    pass


class FailedToProcessTask(UseCaseError):
    pass


class ProcessTaskUseCase(IUseCase[ProcessTaskCommand, ProcessTaskResult]):
    def __init__(
        self, logger: ILogger, transaction_manager: ContextManager[ITransactionManager]
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    def execute(self, command: ProcessTaskCommand) -> ProcessTaskResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Processing task")

        try:
            with self._transaction_manager as tm:
                task = tm.tasks.get_by_id(command.task_id)
                if task is None:
                    use_case_logger.error("Task not found")
                    raise TaskToProcessNotFound

                if task.status in (TaskStatus.DONE, TaskStatus.FAILED):
                    use_case_logger.error("Task already processed")
                    raise TaskAlreadyProcessed

                if task.status != TaskStatus.PROCESSING:
                    task.status = TaskStatus.PROCESSING
                    tm.tasks.save(task)

            task = self._simulate_task_processing(task)

            with self._transaction_manager as tm:
                tm.tasks.save(task)
        except TaskToProcessNotFound:
            raise
        except TaskAlreadyProcessed:
            raise
        except Exception as e:
            use_case_logger.exception("Failed to process task")
            raise FailedToProcessTask from e

        use_case_logger.info(
            "Task processed successfully", context={"new_task_status": task.status}
        )

        return ProcessTaskResult(result=task.result, new_task_status=task.status)

    def _simulate_task_processing(self, task: Task) -> Task:
        time_to_sleep = randint(2, 5)
        sleep(time_to_sleep)

        if task.payload == "fail":
            task.status = TaskStatus.FAILED
        else:
            task.result = str(time_to_sleep)
            task.status = TaskStatus.DONE

        return task
