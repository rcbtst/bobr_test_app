from __future__ import annotations

from typing import Callable, Optional, Type

from sqlalchemy.orm import Session

from src.application.ports import ILogger, ITransactionManager
from src.domain.repositories import ITaskRepository
from src.infrastructure.database.mappers import SQLAlchemyTaskMapper
from src.infrastructure.database.repositories import SQLAlchemyTaskRepository
from src.infrastructure.database.schema import Task


class SQLAlchemyTransactionManager(ITransactionManager):
    def __init__(
        self,
        session_factory: Callable[[], Session],
        logger: ILogger,
    ):
        self.session_factory = session_factory
        self._logger = logger.with_name(__name__)

    def __enter__(self) -> SQLAlchemyTransactionManager:
        self._logger.debug("Starting database transaction")

        try:
            self.session: Session = self.session_factory()

            self.tasks: ITaskRepository = SQLAlchemyTaskRepository(
                self.session, SQLAlchemyTaskMapper(), Task, self._logger
            )

            self.session.begin()

            return self
        except Exception:
            self._logger.exception("Failed to start database transaction")
            raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        try:
            if exc_type is None:
                self._logger.debug("Committing database transaction")
                self.session.commit()
                self._logger.debug("Database transaction committed successfully")
            else:
                self._logger.warning(
                    "Rolling back database transaction",
                    context={
                        "exception_type": exc_type.__name__ if exc_type else None,
                        "exception_message": str(exc_value) if exc_value else None,
                    },
                )
                self.session.rollback()
                self._logger.debug("Database transaction rolled back")
        except Exception:
            self._logger.exception("Error during db transaction cleanup")
            raise
        finally:
            self.session.close()
            self._logger.debug("Database session closed")
