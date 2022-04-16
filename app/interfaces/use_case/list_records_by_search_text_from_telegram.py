import typing
from abc import ABC

from entities.record import Record


class RecordsListBySearchTextFromTelegram(ABC):
    """Interface for filtering records by search text."""

    async def list(self, telegram_id: int, search_text: str, page: int) -> typing.List[Record]:
        """List of records by search_text."""
