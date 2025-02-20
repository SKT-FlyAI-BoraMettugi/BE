from fastapi import APIRouter
from api.routes import user, ranking, question, theme

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=["user"])
api_router.include_router(ranking.router, prefix='/ranking', tags=["ranking"])
api_router.include_router(question.router, prefix='/question', tags=["question"])
api_router.include_router(theme.router, prefix='/theme', tags=["theme"])