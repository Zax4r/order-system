from pydantic import BaseModel, Field
from typing import Optional


class SProductBase(BaseModel):
    name: str


class SProductAdd(SProductBase):
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    stock: Optional[int] = 0


class SProductShow(SProductBase):
    id: int
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    stock: int
