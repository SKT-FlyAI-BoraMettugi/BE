from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.question import save_question, get_question_detail
from schemas.question import QuestionCreate, QuestionResponse
from models.question import Question  

router = APIRouter()

@router.post("/{user_id}")
async def submit_question(user_id: int, question_data: QuestionCreate, db: Session = Depends(get_db)):
    question = save_question(db, user_id, question_data)
    
    return {"message": "문제 출제 완료", "question_id": question.question_id}
    
# 문제 상세 조회
@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    question = get_question_detail(db, question_id)
    
    if not question:
        raise HTTPException(status_code=404, detail="해당 문제를 찾을 수 없습니다.")
    
    return question