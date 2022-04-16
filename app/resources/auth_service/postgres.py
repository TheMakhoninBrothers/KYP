import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import db.postgres as db
from entities.user import TelegramUser
from interfaces.resources.telegram_auth_service import TelegramAuthService


class PostgresTelegramAuthService(TelegramAuthService):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def auth(self, telegram_id: int) -> typing.Optional[TelegramUser]:
        cursor = await self.session.execute(select(db.TelegramUser).where(db.TelegramUser.chat_id == telegram_id))
        user: typing.Optional[db.TelegramUser] = cursor.one_or_none()
        if user:
            return TelegramUser(id=user[0].id, telegram_id=user[0].chat_id, username=user[0].username)
