"""Abstract base for all Data Access Objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseDAO(ABC):
    """Interface every DAO must implement."""

    @abstractmethod
    def save(self, entity: Any) -> None:
        """Persist *entity* in the database."""

    @abstractmethod
    def update(self, entity: Any) -> None:
        """Update an existing record."""

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Delete a record by primary key."""

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[Any]:
        """Return the entity with the given id, or None."""
