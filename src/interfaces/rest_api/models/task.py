from uuid import UUID

from pydantic import BaseModel

from src.domain.enums import TaskStatus


class TaskCreatRequest(BaseModel):
    payload: str


class TaskCreateResponse(BaseModel):
    task_id: UUID


class TaskDataResponse(BaseModel):
    result: str | None = None
    status: TaskStatus
