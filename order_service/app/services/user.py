from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.models.user import User
from app.core.exceptions import CreateError


class UserService(BaseService):
    model = User

    @classmethod
    async def add_user(cls, session: AsyncSession, **user_data):
        try:
            new_user = cls.model(**user_data)
            session.add(new_user)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise CreateError("Ошибка при создании пользователя")