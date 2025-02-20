from fastapi import APIRouter
from api.routes import user, ranking, question, theme, notification, answer, discussion

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=["user"])
api_router.include_router(ranking.router, prefix='/ranking', tags=["ranking"])
api_router.include_router(question.router, prefix='/question', tags=["question"])
api_router.include_router(theme.router, prefix='/theme', tags=["theme"])
api_router.include_router(notification.router, prefix='/notification', tags=["notification"])
api_router.include_router(answer.router, prefix='/answer', tags=["answer"])
api_router.include_router(discussion.router, prefix='/discussion', tags=["discussion"])

