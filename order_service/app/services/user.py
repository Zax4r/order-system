from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.services.base import BaseService
from app.models.user import User

class UserService(BaseService):
    model=User

    @classmethod
    async def add_user(cls,session: AsyncSession, **user_data):
        async with session.begin():
            try:
                new_user = cls.model(**user_data)
                session.add(new_user)
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                return False
            