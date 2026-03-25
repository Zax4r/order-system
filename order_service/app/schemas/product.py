from pydantic import BaseModel
from typing import Optional


class SProductBase(BaseModel):
    name: str

class SProductAdd(SProductBase):
    price: float
    stock: Optional[int] = 0

class SProductShow(SProductBase):
    id: int
    price: float
    stock: int