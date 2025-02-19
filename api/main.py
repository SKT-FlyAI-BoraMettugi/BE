from fastapi import APIRouter
from api.routes import user, ranking

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=["user"])
api_router.include_router(ranking.router, prefix='/ranking', tags=["ranking"])
