import typing
from abc import ABC, abstractmethod

from entities.user import TelegramUser


class RegistrateUserInTelegram(ABC):
    """Interface for registrate users from telegram."""

    @abstractmethod
    async def registrate(self, telegram_id: int, username: typing.Optional[str]) -> TelegramUser:
        """Registrate user in telegram."""
