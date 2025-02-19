from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.user import get_user_info, update_user_nickname
from schemas.nickname import Nickname

router = APIRouter()

@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_info(db, user_id)
    return user

@router.patch('/nickname/{user_id}')
async def update_nickname(nickname: Nickname, db: Session = Depends(get_db)):
    update_user_nickname(nickname, db)
    return nickname