from typing import Optional

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums import TaskStatus
from src.infrastructure.database.schema.base import Base, CreatedUpdatedAtMixin, IdMixin


class Task(IdMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "tasks"

    payload: Mapped[str]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"), default=TaskStatus.PENDING
    )
    result: Mapped[Optional[str]]
    dispatched: Mapped[bool] = mapped_column(default=False)
