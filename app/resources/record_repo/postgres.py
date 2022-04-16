import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import db.postgres as db
from entities.record import Record
from entities.tag import Tag
from entities.user import TelegramUser
from interfaces.exc.entity import EntityNotExist
from interfaces.resources.record_repo import RecordRepo


class PostgresRecordRepo(RecordRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, owner_id: int, text: str, tag_ids: typing.List[int]) -> Record:
        cursor = await self.session.execute(select(db.Tag).where(db.Tag.id.in_(tag_ids), db.Tag.owner_id == owner_id))
        tags = [tag[0] for tag in cursor.all()]
        new_record = db.Record(text=text, tags=tags, owner_id=owner_id)
        self.session.add(new_record)
        await self.session.commit()
        cursor = await self.session.execute(select(db.TelegramUser).where(db.TelegramUser.id == owner_id))
        owner = cursor.one()
        return Record(
            id=new_record.id,
            text=text,
            tags=[Tag(id=tag.id, name=tag.name) for tag in tags],
            owner=TelegramUser(
                id=owner[0].id,
                telegram_id=owner[0].chat_id,
                username=owner[0].username,
            ),
            created_at=new_record.created_at,
        )

    async def find(self, record_id: str) -> Record:
        query = select(db.Record).where(db.Record.id == record_id)
        cursor = await self.session.execute(query)
        record_from_db: typing.Optional[db.Record] = cursor.one_or_none()
        if not record_from_db:
            raise EntityNotExist()
        return Record(
            id=record_from_db.id,
            text=record_from_db.text,
            tags=[Tag(id=tag.id, name=tag.name) for tag in record_from_db.tags],
            owner=TelegramUser(
                id=record_from_db.owner.id,
                telegram_id=record_from_db.owner.chat_id,
                username=record_from_db.owner.usenrame,
            ),
            created_at=record_from_db.created_at,
        )

    async def list(
            self,
            owner_id: typing.Optional[int] = None,
            tag_ids: typing.Optional[typing.List[int]] = None,
            limit: int = 5,
            offset: int = 0,
    ) -> typing.List[Record]:
        query = select(db.Record).join(db.TelegramUser)
        if owner_id:
            query = query.where(db.TelegramUser.id == owner_id)
        query = query.limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        records_from_db = cursor.all()
        if tag_ids:
            records = [
                record_from_db for record_from_db in records_from_db
                if set(tag_ids) == {tag.id for tag in record_from_db[0].tags}.intersection(set(tag_ids))
            ]  # TODO: Спрятать в SQL
        else:
            records = records_from_db
        return [
            Record(
                id=record_from_db[0].id,
                text=record_from_db[0].text,
                tags=[Tag(id=tag.id, name=tag.name) for tag in record_from_db[0].tags],
                owner=TelegramUser(
                    id=record_from_db[0].owner.id,
                    telegram_id=record_from_db[0].owner.chat_id,
                    username=record_from_db[0].owner.username,
                ),
                created_at=record_from_db[0].created_at,
            )
            for record_from_db in records
        ]
