from fastapi import APIRouter, Depends
from app.schemas.order import SOrderAdd, SOrderShow
from typing import List
from app.database import get_db
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get("/", response_model=List[SOrderShow])
async def get_all(session=Depends(get_db)):
    return await OrderService.get_all(session)


@router.post("/add/")
async def add_order(new_order: SOrderAdd, session=Depends(get_db)):
    await OrderService.add_order(session, **new_order.model_dump())
    return new_order


@router.delete("/delete/{id}")
async def delete_order(id: int, session=Depends(get_db)):
    await OrderService.delete_by_id(session, id)
    return {"message": f"Заказ {id} удалён"}
