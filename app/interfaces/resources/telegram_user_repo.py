import typing
from abc import ABC, abstractmethod

from entities.user import TelegramUser


class TelegramUserRepo(ABC):
    """Interface of telegram users repository."""

    @abstractmethod
    async def add(
            self,
            telegram_id: int,
            username: typing.Optional[str],
    ) -> TelegramUser:
        """Add user from telegram."""

    @abstractmethod
    async def find(self, telegram_id: int) -> TelegramUser:
        """Find telegram user by chat_id from telegram.
        If user was not found than raise EntityNotExist.
        """

    @abstractmethod
    async def list(self, limit: int = 5, offset: int = 0) -> typing.List[TelegramUser]:
        """Find list of users."""
