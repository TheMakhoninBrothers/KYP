import typing
from abc import ABC, abstractmethod

from entities.record import Record


class RecordRepo(ABC):
    """Interface of records repository."""

    @abstractmethod
    async def add(self, telegram_id: int, tags: typing.List[str]) -> Record:
        """Add record in repository.
        Tags - list of text.
        """

    @abstractmethod
    async def find(self, record_id: str) -> Record:
        """Find record by id.
        If record was not found than raise EntityNotExist.
        """

    @abstractmethod
    async def list(self, owner: typing.Optional[int] = None, limit: int = 5, offset: int = 0) -> typing.List[Record]:
        """Find list of records.
        Filter by:
            - owner: chat_id in telegram.
        """
