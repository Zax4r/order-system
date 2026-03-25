from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import List


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)

    orders: Mapped[List["Order"]] = relationship(back_populates="product")
