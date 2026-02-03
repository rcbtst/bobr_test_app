from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from src.application.ports import ILogger
from src.domain.repositories.base import IRepository
from src.infrastructure.database.mappers.base import IDBMapper

D = TypeVar("D")
O = TypeVar("O")


class SQLAlchemyRepository(Generic[O, D], IRepository[D]):
    def __init__(
        self,
        session: Session,
        mapper: IDBMapper[D, O],
        model: Type[O],
        logger: ILogger,
    ):
        self.session = session
        self.mapper = mapper
        self.model = model
        self._logger = logger.with_name(__name__)

    def save(self, obj: D) -> None:
        logger = self._logger.with_context({"model": self.model.__name__})

        logger.debug("Saving object to db")
        try:
            orm_obj = self.mapper.to_orm(obj)
            self.session.merge(orm_obj)
            self.session.flush()
            logger.info("Object saved to db")
        except Exception:
            logger.exception("Failed to save object to db")
            raise

    def get_by_id(self, obj_id: UUID) -> D | None:
        logger = self._logger.with_context(
            {
                "obj_id": str(obj_id),
                "model": self.model.__name__,
            }
        )
        logger.debug("Getting object by id from db")
        try:
            orm_obj = self.session.get(self.model, obj_id)
            if not orm_obj:
                logger.debug("Object not found in db")
                return None

            return self.mapper.to_domain(orm_obj)
        except Exception:
            logger.exception("Failed to get object by id from db")
            raise
