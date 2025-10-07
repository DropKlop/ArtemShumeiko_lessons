from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.DB_URL)
engine_null_pull = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_sessionmaker_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_sessionmaker_maker_null_pull = async_sessionmaker(
    bind=engine_null_pull, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
