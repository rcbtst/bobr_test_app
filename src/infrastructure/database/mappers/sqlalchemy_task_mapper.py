from src.domain.entities import Task as TaskDomain
from src.infrastructure.database.mappers.base import IDBMapper
from src.infrastructure.database.schema import Task as TaskORM


class SQLAlchemyTaskMapper(IDBMapper[TaskDomain, TaskORM]):
    def to_orm(self, domain_obj: TaskDomain) -> TaskORM:
        return TaskORM(
            id=domain_obj.id,
            payload=domain_obj.payload,
            status=domain_obj.status,
            result=domain_obj.result,
            dispatched=domain_obj.dispatched,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
        )

    def to_domain(self, orm_obj: TaskORM) -> TaskDomain:
        return TaskDomain(
            id=orm_obj.id,
            payload=orm_obj.payload,
            status=orm_obj.status,
            result=orm_obj.result,
            dispatched=orm_obj.dispatched,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )
