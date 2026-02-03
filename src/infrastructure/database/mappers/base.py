from abc import ABC, abstractmethod
from typing import Generic, TypeVar

D = TypeVar("D")
O = TypeVar("O")


class IDBMapper(ABC, Generic[D, O]):
    @abstractmethod
    def to_orm(self, domain_obj: D) -> O:
        """
        Map a domain object to an ORM instance.
        """
        pass

    @abstractmethod
    def to_domain(self, orm_obj: O) -> D:
        """
        Map an ORM instance to a domain object.
        """
        pass
