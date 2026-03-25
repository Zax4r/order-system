from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.user import SUserAdd, SUserShow
from typing import List
from app.database import get_db
from app.services.user import UserService


router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.get('/', response_model=List[SUserShow])
async def get_all(session=Depends(get_db)):
    users = await UserService.get_all(session)
    return users

@router.post('/add/')
async def add_user(new_user: SUserAdd, session=Depends(get_db)):
    res = await UserService.add_user(session, **new_user.model_dump())
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Ошибка при добавлении пользователя')
    return new_user
