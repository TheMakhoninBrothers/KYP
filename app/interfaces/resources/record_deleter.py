from abc import ABC, abstractmethod


class RecordDeleter(ABC):
    """Interface of record deleter."""

    @abstractmethod
    async def delete(self, record_id: int):
        """Delete record by id from storage."""
