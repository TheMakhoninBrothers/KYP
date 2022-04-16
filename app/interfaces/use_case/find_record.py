from abc import ABC, abstractmethod

from entities.record import Record


class FindRecord(ABC):
    """Interface for find record in storage."""

    @abstractmethod
    async def find(self, record_id: int) -> Record:
        """Find record"""
