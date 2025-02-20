from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.answer import get_answer_history
from schemas.answer import AnswerResponse

router = APIRouter()

@router.get("/history/{user_id}/{question_id}", response_model=list[AnswerResponse])
async def get_answer_history_api(user_id: int, question_id: int, db: Session = Depends(get_db)):
    answers = get_answer_history(db, user_id, question_id)
    
    if not answers:
        raise HTTPException(status_code=404, detail="답변 이력이 없습니다.")

    return answers
