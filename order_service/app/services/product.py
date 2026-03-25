from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.models.product import Product
from app.core.exceptions import CreateError


class ProductService(BaseService):
    model = Product

    @classmethod
    async def add_product(cls, session: AsyncSession, **product_data):
        try:
            new_product = cls.model(**product_data)
            session.add(new_product)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise CreateError("Ошибка при создании товара")