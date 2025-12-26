from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from .config import settings

SQL_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_async_engine(
    SQL_DATABASE_URL,
    echo=True
)

SeassionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SeassionLocal() as session:
        try:
            yield session
        finally:
            await session.close()