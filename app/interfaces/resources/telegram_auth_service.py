import typing
from abc import ABC, abstractmethod

from entities.user import TelegramUser


class TelegramAuthService(ABC):
    """Interface for auth in telegram"""

    @abstractmethod
    async def auth(self, telegram_id: int) -> typing.Optional[TelegramUser]:
        """Authorization."""
