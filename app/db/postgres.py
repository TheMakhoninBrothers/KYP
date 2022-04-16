import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import configs


class PostgresAsyncEngine:

    def __init__(self, url):
        self.engine = create_async_engine(url)


async_engine = PostgresAsyncEngine(configs.POSTGRES_URI).engine
Base = declarative_base()


def session_factory():
    async_engine = create_async_engine(configs.POSTGRES_URI)
    return sessionmaker(async_engine, future=True, expire_on_commit=False, class_=AsyncSession)()


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id = sql.Column(sql.Integer, primary_key=True)

    chat_id = sql.Column(sql.Integer, unique=True, nullable=False)
    username = sql.Column(sql.VARCHAR(100))
