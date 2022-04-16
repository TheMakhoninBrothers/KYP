from abc import ABC, abstractmethod

from entities.record import Record


class AddRecordInUserStorageFromTelegram(ABC):
    """Interface for add record by telegram user."""

    @abstractmethod
    async def add(self, telegram_id: int, text: str) -> Record:
        """Add record in user storage"""
