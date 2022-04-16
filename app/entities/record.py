import typing
from dataclasses import dataclass
from datetime import datetime

from entities.tag import Tag
from entities.user import TelegramUser


@dataclass
class Record:
    """Record entity"""
    id: int
    text: str
    tags: typing.List[Tag]
    owner: TelegramUser
    created_at: datetime
