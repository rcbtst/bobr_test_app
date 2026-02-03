from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.application.contracts.create_task import CreateTaskCommand, CreateTaskResult
from src.application.contracts.get_task import GetTaskCommand, GetTaskResult
from src.application.use_cases.get_task import TaskNotFound
from src.interfaces.rest_api.dependencies import CreateTaskUseCaseDep, GetTaskUseCaseDep
from src.interfaces.rest_api.models import (
    TaskCreateResponse,
    TaskCreatRequest,
    TaskDataResponse,
)

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


@router.get("/{task_id}", responses={404: {"description": "Task not found"}})
def get_task(task_id: UUID, get_task_use_case: GetTaskUseCaseDep) -> TaskDataResponse:
    try:
        result: GetTaskResult = get_task_use_case(GetTaskCommand(task_id=task_id))
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return TaskDataResponse(result=result.result, status=result.status)
