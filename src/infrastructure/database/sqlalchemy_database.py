from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from src.application.ports import ILogger


class SQLAlchemyDatabase:
    def __init__(self, url: str | URL, logger: ILogger, **engine_kwargs: dict) -> None:
        self._logger = logger.with_name(__name__)
        self._logger.debug("Creating SQLAlchemy engine")

        self._engine = create_engine(url, **engine_kwargs)
        self._session_factory: sessionmaker[Session] = sessionmaker(
            self._engine, expire_on_commit=False
        )

    @property
    def session_factory(self) -> sessionmaker[Session]:
        return self._session_factory

    def dispose(self) -> None:
        self._logger.debug("Disposing SQLAlchemy engine")
        self._engine.dispose()
