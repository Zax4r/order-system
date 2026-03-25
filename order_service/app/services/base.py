from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        stmt = select(cls.model).filter_by(**filters)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id):
        query = await session.execute(select(cls.model).where(cls.model.id == id))
        entity = query.scalar_one_or_none()
        if not entity:
            raise NotFoundError(f"{cls.model.__name__} с id={id} не найден")
        await session.delete(entity)
        await session.commit()
