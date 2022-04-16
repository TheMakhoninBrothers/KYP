import typing

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import db.postgres as db
from entities.tag import Tag
from interfaces.exc.entity import EntityAlreadyExist, EntityNotExist
from interfaces.resources.tag_repo import TagRepo


class PostgresTagRepo(TagRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, owner_id: int, name: str) -> Tag:
        query = select(db.Tag).where(db.Tag.owner_id == owner_id, db.Tag.name == name)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise EntityAlreadyExist()
        new_tag = db.Tag(owner_id=owner_id, name=name)
        self.session.add(new_tag)
        await self.session.commit()
        return Tag(id=new_tag.id, name=new_tag.name)

    async def find(self, tag_id: str) -> Tag:
        query = select(db.Tag).where(db.Tag.id == tag_id)
        cursor = await self.session.execute(query)
        tag_from_db: typing.Optional[Tag] = cursor.one_or_none()
        if not tag_from_db:
            raise EntityNotExist()
        return Tag(id=tag_from_db.id, name=tag_from_db.name)

    async def list(self, owner_id: typing.Optional[int] = None, limit: int = 5, offset: int = 0) -> typing.List[Tag]:
        query = select(db.Tag)
        if owner_id:
            query = query.where(db.Tag.owner_id == owner_id)
        query = query.limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        return [Tag(id=tag_from_db[0].id, name=tag_from_db[0].name) for tag_from_db in cursor.all()]
