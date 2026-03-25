from pydantic import BaseModel
from typing import Optional


class SOrderBase(BaseModel):
    quantity: int

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