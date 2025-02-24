from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.comment import create_comment, add_like_to_comment, get_liked_comments_by_user
from schemas.comment import CommentCreate, CommentResponse, CommentLikeResponse

router = APIRouter()

# 토론에 대한 답글 생성
@router.post("/{user_id}/{discussion_id}", response_model=CommentResponse)
async def post_comment(user_id: int, discussion_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    comment = create_comment(db, user_id, discussion_id, comment_data)
    return comment

# 답글 좋아요
@router.patch("/like/{comment_id}/{user_id}", response_model=CommentLikeResponse)
async def like_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    comment = add_like_to_comment(db, comment_id, user_id)
    return comment

# 좋아요 누른 답글 조회
@router.get("/like/{user_id}")
async def get_liked_comments(user_id: int, db: Session = Depends(get_db)):
    return get_liked_comments_by_user(db, user_id)