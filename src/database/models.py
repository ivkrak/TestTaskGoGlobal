import os

from sqlalchemy import BigInteger, Column, String, Integer, Float
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_async_engine(
    f'postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@db:5432/{os.getenv("DB_NAME")}')  # NOQA

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # NOQA

metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    tg_user_id = Column(BigInteger, primary_key=True)
    tg_name = Column(String(255))
    subscribe = Column(Integer, default=0)


class ExchangeHistory(Base):
    __tablename__ = 'exchange_history'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    tg_user_id = Column(BigInteger)
    request_time = Column(Float)
    exchange = Column(Float)
