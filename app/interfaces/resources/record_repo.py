import typing
from abc import ABC, abstractmethod

from entities.record import Record


class RecordRepo(ABC):
    """Interface of records repository."""

    @abstractmethod
    async def add(self, owner_id: int, text: str, tag_ids: typing.List[int]) -> Record:
        """Add record in repository.
        Tags - list of text.
        """

    @abstractmethod
    async def find(self, record_id: int) -> Record:
        """Find record by id.
        If record was not found than raise EntityNotExist.
        """

    @abstractmethod
    async def list(
            self,
            owner_id: typing.Optional[int] = None,
            tag_ids: typing.Optional[typing.List[int]] = None,
            limit: int = 5,
            offset: int = 0,
    ) -> typing.List[Record]:
        """Find list of records.
        Filter by:
            - owner: id in storage.
        """
