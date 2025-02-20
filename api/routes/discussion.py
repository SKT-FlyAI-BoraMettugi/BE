from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.discussion import create_discussion
from schemas.discussion import DiscussionCreate, DiscussionResponse

router = APIRouter()

@router.post("/{user_id}/{question_id}", response_model=DiscussionResponse)
async def submit_discussion(user_id: int, question_id: int, discussion_data: DiscussionCreate, db: Session = Depends(get_db)):
    discussion = create_discussion(db, user_id, question_id, discussion_data)
    return discussion
