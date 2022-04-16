import typing
from dataclasses import dataclass


@dataclass
class TelegramUser:
    """Telegram user entity"""
    telegram_id: int
    username: typing.Optional[str]
