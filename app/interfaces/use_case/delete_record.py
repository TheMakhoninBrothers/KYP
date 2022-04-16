from abc import ABC, abstractmethod


class DeleteRecord(ABC):
    """Interface for delete record"""

    @abstractmethod
    async def delete(self, record_id: int):
        """Delete record from user storage"""
