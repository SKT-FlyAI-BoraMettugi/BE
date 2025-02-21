from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.comment import create_comment
from schemas.comment import CommentCreate, CommentResponse

router = APIRouter()

# 토론에 대한 답글 생성
@router.post("/{user_id}/{discussion_id}", response_model=CommentResponse)
async def post_comment(user_id: int, discussion_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    comment = create_comment(db, user_id, discussion_id, comment_data)
    return comment
