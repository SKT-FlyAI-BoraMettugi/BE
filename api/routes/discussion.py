from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.discussion import create_discussion, get_discussions_by_question, add_like_to_discussion, get_liked_discussions_by_user
from schemas.discussion import DiscussionCreate, DiscussionResponse, DiscussionLikeResponse
from typing import List

router = APIRouter()

# 토론 생성 
@router.post("/{user_id}/{question_id}", response_model=DiscussionResponse)
async def submit_discussion(user_id: int, question_id: int, discussion_data: DiscussionCreate, db: Session = Depends(get_db)):
    discussion = create_discussion(db, user_id, question_id, discussion_data)
    return discussion

#  토론 내용 조회
@router.get("/{question_id}", response_model=list[DiscussionResponse])
async def get_discussions(question_id: int, db: Session = Depends(get_db)):
    discussions = get_discussions_by_question(db, question_id)

    if not discussions:
        raise HTTPException(status_code=404, detail="해당 문제에 대한 토론이 없습니다.")

    return discussions

# 토론 좋아요 추가
@router.patch("/like/{discussion_id}/{user_id}", response_model=DiscussionLikeResponse)
async def like_discussion(discussion_id: int, user_id: int, db: Session = Depends(get_db)):
    result = add_like_to_discussion(db, discussion_id, user_id)
    return result

# 좋아요 누른 토론 조회
@router.get("/like/{user_id}", response_model=List[DiscussionResponse])
async def get_liked_discussions(user_id: int, db: Session = Depends(get_db)):
    liked_discussions = get_liked_discussions_by_user(db, user_id)

    if not liked_discussions:
        raise HTTPException(status_code=404, detail="좋아요 누른 토론이 없습니다.")

    return liked_discussions
    