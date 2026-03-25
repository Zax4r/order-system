from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.user import router as user_router
from app.routers.product import router as product_router
from app.routers.order import router as order_router
from app.core.exceptions import AppException

app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get('/')
async def root():
    return {'msg': 'Hello world'}