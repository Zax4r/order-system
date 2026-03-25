from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.core.config import get_db_url

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase, AsyncAttrs):
    pass

async def get_db():
    async with Session() as session:
        yield session