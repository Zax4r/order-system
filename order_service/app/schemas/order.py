from pydantic import BaseModel, Field
from typing import Optional


class SOrderBase(BaseModel):
    quantity: int = Field(gt=0, description="Количество должно быть больше 0")


class SOrderAdd(SOrderBase):
    user_id: int
    product_id: int
    status: Optional[str] = None


class SOrderShow(BaseModel):
    id: int
    username: str
    product_name: str
    quantity: int
    status: str
