from dependency_injector import containers, providers
from sqlalchemy.engine import URL

from src.application.use_cases import (
    CreateTaskUseCase,
    GetNotDispatchedTasksUseCase,
    GetTaskUseCase,
    MarkTasksAsDispatchedUseCase,
)
from src.application.use_cases.process_task import ProcessTaskUseCase
from src.config import settings
from src.infrastructure.database import SQLAlchemyDatabase, SQLAlchemyTransactionManager
from src.infrastructure.utils import StdLibLogger


def _build_db_url() -> URL:
    return URL.create(
        drivername=settings.DB_DRIVER,
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD.get_secret_value(),
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )


class ApplicationContainer(containers.DeclarativeContainer):
    logger = providers.Factory(StdLibLogger)

    db = providers.Singleton(
        SQLAlchemyDatabase,
        url=providers.Callable(_build_db_url),
        logger=logger,
        echo=False,
        pool_pre_ping=True,
    )

    transaction_manager = providers.Factory(
        SQLAlchemyTransactionManager,
        session_factory=db.provided.session_factory,
        logger=logger,
    )

    create_task_use_case = providers.Factory(
        CreateTaskUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )

    get_not_dispatched_tasks_use_case = providers.Factory(
        GetNotDispatchedTasksUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )

    mark_tasks_as_dispatched_use_case = providers.Factory(
        MarkTasksAsDispatchedUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )

    process_task_use_case = providers.Factory(
        ProcessTaskUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )

    get_task_use_case = providers.Factory(
        GetTaskUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )
