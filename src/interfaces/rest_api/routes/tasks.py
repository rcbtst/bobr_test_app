from fastapi import APIRouter, status

from src.application.contracts.create_task import CreateTaskCommand, CreateTaskResult
from src.interfaces.rest_api.dependencies import CreateTaskUseCaseDep
from src.interfaces.rest_api.models import TaskCreateResponse, TaskCreatRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_new_task(
    input_data: TaskCreatRequest,
    create_task_use_case: CreateTaskUseCaseDep,
) -> TaskCreateResponse:
    result: CreateTaskResult = create_task_use_case(
        CreateTaskCommand(payload=input_data.payload)
    )

    return TaskCreateResponse(task_id=result.new_task_id)
