import uuid
import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.services.base import BaseService
from app.models.order import Order
from app.models.outbox import Outbox
from app.schemas.order import SOrderShow
from app.core.exceptions import CreateError


class OrderService(BaseService):
    model = Order

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        stmt = (
            select(Order)
            .options(selectinload(Order.user), selectinload(Order.product))
            .filter_by(**filters)
        )
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return [
            SOrderShow(
                id=o.id,
                username=o.user.username,
                product_name=o.product.name,
                quantity=o.quantity,
                status=o.status,
            )
            for o in orders
        ]

    @classmethod
    async def add_order(cls, session: AsyncSession, **order_data):
        async with session.begin():
            try:
                new_order = Order(**order_data)
                session.add(new_order)
                await session.flush()

                new_outbox = Outbox(
                    event_type="order.created",
                    payload={
                        "order_id": new_order.id,
                        "user_id": new_order.user_id,
                        "product_id": new_order.product_id,
                        "quantity": new_order.quantity,
                        "event_id": str(uuid.uuid4()),
                        "timestamp": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat(),
                    },
                    sent=False,
                )
                session.add(new_outbox)
                await session.commit()

            except IntegrityError:
                await session.rollback()
                raise CreateError(
                    "Ошибка при создании заказа: неверный user_id или product_id"
                )
