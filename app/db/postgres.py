from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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

    records = relationship('Record', back_populates='owner')
    tags = relationship('Tag', back_populates='owner')


pivot_records_tags = sql.Table(
    'pivot_records_tags',
    Base.metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('record_id', sql.ForeignKey('records.id')),
    sql.Column('tag_id', sql.ForeignKey('tags.id')),
)


class Record(Base):
    __tablename__ = 'records'

    id = sql.Column(sql.Integer, primary_key=True)
    text = sql.Column(sql.String, nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey('telegram_users.id'))

    owner = relationship('TelegramUser', back_populates='records', lazy='selectin')
    tags = relationship('Tag', secondary=pivot_records_tags, back_populates='records', lazy='selectin')


class Tag(Base):
    __tablename__ = 'tags'

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.VARCHAR(100), nullable=False)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey('telegram_users.id'))

    owner = relationship('TelegramUser', back_populates='tags')
    records = relationship('Record', secondary=pivot_records_tags, back_populates='tags')
