import typing
from abc import ABC, abstractmethod

from entities.tag import Tag


class TagRepo(ABC):
    """Interface of tags repository."""

    @abstractmethod
    async def add(self, telegram_id: int, text: str) -> Tag:
        """Add tag in repository.
        Tags - list of text.
        """

    @abstractmethod
    async def find(self, tag_id: str) -> Tag:
        """Find tag by id.
        If tag was not found than raise EntityNotExist.
        """

    @abstractmethod
    async def list(self, owner: typing.Optional[int] = None, limit: int = 5, offset: int = 0) -> typing.List[Tag]:
        """Find list of tags.
        Filter by:
            - owner: chat_id in telegram.
        """
