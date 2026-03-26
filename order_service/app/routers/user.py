from fastapi import APIRouter, Depends
from app.schemas.user import SUserAdd, SUserShow
from typing import List
from app.database import get_db
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/", response_model=List[SUserShow])
async def get_all(session=Depends(get_db)):
    return await UserService.get_all(session)


@router.post("/add/")
async def add_user(new_user: SUserAdd, session=Depends(get_db)):
    await UserService.add_user(session, **new_user.model_dump())
    return new_user


@router.delete("/delete/{id}")
async def delete_user(id: int, session=Depends(get_db)):
    await UserService.delete_by_id(session, id)
    return {"message": f"Пользователь {id} удалён"}
