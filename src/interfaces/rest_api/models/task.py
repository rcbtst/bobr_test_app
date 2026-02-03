from uuid import UUID

from pydantic import BaseModel


class TaskCreatRequest(BaseModel):
    payload: str


class TaskCreateResponse(BaseModel):
    task_id: UUID
