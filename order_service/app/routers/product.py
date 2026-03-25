from fastapi import APIRouter, Depends
from app.schemas.product import SProductAdd, SProductShow
from typing import List
from app.database import get_db
from app.services.product import ProductService


router = APIRouter(prefix='/products', tags=['Товары'])


@router.get('/', response_model=List[SProductShow])
async def get_all(session=Depends(get_db)):
    return await ProductService.get_all(session)


@router.post('/add/')
async def add_product(new_product: SProductAdd, session=Depends(get_db)):
    await ProductService.add_product(session, **new_product.model_dump())
    return new_product


@router.delete('/delete/{id}')
async def delete_product(id: int, session=Depends(get_db)):
    await ProductService.delete_by_id(session, id)
    return {'message': f'Товар {id} удалён'}