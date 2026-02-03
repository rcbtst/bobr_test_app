from uuid import UUID

from celery import shared_task
from dependency_injector.wiring import Provide, inject

from src.application.contracts.process_task import ProcessTaskCommand
from src.application.use_cases import ProcessTaskUseCase
from src.application.use_cases.process_task import TaskAlreadyProcessed
from src.infrastructure.di_config import ApplicationContainer


@shared_task(
    name="process_new_task",
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=10,
    retry_jitter=True,
)
@inject
def process_new_task_task(
    task_id: UUID,
    process_task_use_case: ProcessTaskUseCase = Provide[
        ApplicationContainer.process_task_use_case
    ],
):
    try:
        process_task_use_case(ProcessTaskCommand(task_id=task_id))
    except TaskAlreadyProcessed:
        pass
