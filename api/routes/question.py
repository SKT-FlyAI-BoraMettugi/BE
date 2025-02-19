from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.question import save_question
from schemas.question import QuestionCreate
from models.question import Question  

router = APIRouter()

@router.post("/{user_id}")
async def submit_question(user_id: int, question_data: QuestionCreate, db: Session = Depends(get_db)):
    # 사용자 출제 문제 (False)
    question_type = question_data.question_type if question_data.question_type is not None else False
    
    new_question = Question(
        user_id=user_id,
        question_type=question_type,
        title=question_data.title,
        question=question_data.question,
        answer=question_data.answer
    )

    # 테마 문제일 경우 (question_type=True) ->  step, difficulty 추가
    if question_type:
        new_question.step = question_data.step
        new_question.difficulty = question_data.difficulty
    else:
        # 사용자 출제 문제일 경우 -> 기본 필드 설정
        new_question.is_approved = False
        new_question.is_chosen = False
        new_question.is_active = False

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "message": "문제 출제 완료",
        "question_id": new_question.id
    }
