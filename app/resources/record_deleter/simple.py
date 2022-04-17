from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

import db.postgres as db
from interfaces.exc.entity import EntityNotExist
from interfaces.resources.record_deleter import RecordDeleter as Interface


class RecordDeleter(Interface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, record_id: int):
        query = select(db.Record).where(db.Record.id == record_id)
        cursor = await self.session.execute(query)
        if not cursor.one_or_none():
            raise EntityNotExist()
        query = delete(db.Record).where(db.Record.id == record_id)
        await self.session.execute(query)
        await self.session.commit()
