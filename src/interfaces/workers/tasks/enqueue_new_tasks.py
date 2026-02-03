from celery import shared_task
from dependency_injector.wiring import Provide, inject

from src.application.contracts.get_not_dispatched_tasks import (
    GetNotDispatchedTasksCommand,
    GetNotDispatchedTasksResult,
)
from src.application.contracts.mark_tasks_as_dispatched import (
    MarkTasksAsDispatchedCommand,
)
from src.application.use_cases import (
    GetNotDispatchedTasksUseCase,
    MarkTasksAsDispatchedUseCase,
)
from src.config import settings
from src.infrastructure.di_config import ApplicationContainer
from src.interfaces.workers.tasks.process_new_task import process_new_task_task


@shared_task(name="enqueue_new_tasks")
@inject
def enqueue_new_tasks_task(
    get_not_dispatched_tasks_use_case: GetNotDispatchedTasksUseCase = Provide[
        ApplicationContainer.get_not_dispatched_tasks_use_case
    ],
    mark_tasks_as_dispatched_use_case: MarkTasksAsDispatchedUseCase = Provide[
        ApplicationContainer.mark_tasks_as_dispatched_use_case
    ],
):
    get_not_dispatched_tasks_result: GetNotDispatchedTasksResult = (
        get_not_dispatched_tasks_use_case(
            GetNotDispatchedTasksCommand(
                limit=settings.APP_MAX_PENDING_TASKS_TO_ENQUEUE_AT_ONCE
            )
        )
    )
    if get_not_dispatched_tasks_result.not_dispatched_task_ids:
        for task_id in get_not_dispatched_tasks_result.not_dispatched_task_ids:
            process_new_task_task.delay(task_id=task_id)

        mark_tasks_as_dispatched_use_case(
            MarkTasksAsDispatchedCommand(
                task_ids=get_not_dispatched_tasks_result.not_dispatched_task_ids
            )
        )
