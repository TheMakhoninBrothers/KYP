import typing
from abc import ABC

from entities.user import TelegramUser


class TelegramAuthService(ABC):
    """Interface for auth in telegram"""

    def auth(self, telegram_id: int) -> typing.Optional[TelegramUser]:
        """Authorization."""
