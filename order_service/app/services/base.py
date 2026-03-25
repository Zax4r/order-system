from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        stmt = select(cls.model).filter_by(**filters)
        query = await session.execute(stmt)
        res = query.scalars().all()
        return res
        
            
        