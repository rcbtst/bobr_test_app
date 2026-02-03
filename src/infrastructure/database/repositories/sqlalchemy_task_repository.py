from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update

from src.domain.entities import Task
from src.domain.repositories import ITaskRepository
from src.infrastructure.database.repositories.sqlalchemy_repository import (
    SQLAlchemyRepository,
)
from src.infrastructure.database.schema import Task as TaskORM


class SQLAlchemyTaskRepository(SQLAlchemyRepository[TaskORM, Task], ITaskRepository):
    def get_all_not_dispatched_ids(self, limit: int | None = None) -> list[UUID]:
        logger = self._logger.with_context({"limit": limit})
        logger.debug("Getting all not dispatched tasks from db")

        try:
            result = self.session.scalars(
                select(TaskORM.id).where(TaskORM.dispatched.is_(False)).limit(limit)
            )

            return list(result.all())
        except Exception:
            logger.exception("Failed to get all not dispatched tasks from db")
            raise

    def mark_as_dispatched(self, task_ids: list[UUID]) -> None:
        logger = self._logger.with_context(
            {"task_ids": [str(task_id) for task_id in task_ids]}
        )
        logger.debug("Marking tasks as dispatched in db")

        try:
            result = self.session.execute(
                update(TaskORM)
                .where(
                    TaskORM.id.in_(task_ids),
                    TaskORM.dispatched.is_(False),
                )
                .values(
                    dispatched=True,
                    updated_at=datetime.now(tz=UTC),
                )
            )
            if result.rowcount:
                logger.info("Tasks marked as dispatched in db successfully")
        except Exception:
            logger.exception("Failed to mark tasks as dispatched in db")
            raise
