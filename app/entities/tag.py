from dataclasses import dataclass

from entities.user import TelegramUser


@dataclass
class Tag:
    """Tag entity"""
    id: int
    name: str
