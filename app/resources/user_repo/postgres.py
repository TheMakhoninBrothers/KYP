import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import db.postgres as db
from entities.user import TelegramUser
from interfaces.exc.entity import EntityAlreadyExist, EntityNotExist
from interfaces.resources.telegram_user_repo import TelegramUserRepo


class PostgresTelegramUserRepo(TelegramUserRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(
            self,
            telegram_id: int,
            username: typing.Optional[str],
    ) -> TelegramUser:
        query = select(db.TelegramUser).where(db.TelegramUser.chat_id == telegram_id)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise EntityAlreadyExist()
        self.session.add(db.TelegramUser(chat_id=telegram_id, username=username))
        return TelegramUser(telegram_id=telegram_id, username=username)

    async def find(self, telegram_id: int) -> TelegramUser:
        query = select(db.TelegramUser).where(db.TelegramUser.chat_id == telegram_id)
        cursor = await self.session.execute(query)
        user_from_db: typing.Optional[db.TelegramUser] = cursor.one_or_none()
        if not user_from_db:
            raise EntityNotExist()
        return TelegramUser(telegram_id=user_from_db[0].chat_id, username=user_from_db[0].username)

    async def list(self, limit: int = 5, offset: int = 0) -> typing.List[TelegramUser]:
        query = select(db.TelegramUser).limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        return [
            TelegramUser(telegram_id=user_from_db[0].chat_id, username=user_from_db[0].username)
            for user_from_db in cursor.all()
        ]
