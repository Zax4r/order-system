from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.services.base import BaseService
from app.models.order import Order
from app.schemas.order import SOrderShow
from app.core.exceptions import CreateError


class OrderService(BaseService):
    model = Order

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        stmt = (select(Order).options(selectinload(Order.user), selectinload(Order.product))
        )
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return [SOrderShow(
                id=o.id,
                username=o.user.username,
                product_name=o.product.name,
                quantity=o.quantity,
                status=o.status,
            )
            for o in orders]

    @classmethod
    async def add_order(cls, session: AsyncSession, **order_data):
        try:
            new_order = cls.model(**order_data)
            session.add(new_order)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise CreateError("Ошибка при создании заказа: неверный user_id или product_id")