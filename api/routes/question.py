from fastapi import APIRouter, Depends, HTTPException
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



@router.get("/{question_id}")
async def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()

    # 문제를 찾을 수 없을 경우 
    if not question:
        raise HTTPException(status_code=404, detail="해당 문제를 찾을 수 없습니다.")

    # JSON 응답 반환
    return {
        "question_id": question.id,
        "user_id": question.user_id,
        "question_type": True if question.question_type else False,
        # "theme_id": ,
        "title": question.title,
        "question": question.question,
        "answer": question.answer,
        "image_url": question.image_url,
        "is_approved": question.is_approved if not question.question_type else None,
        "is_chosen": question.is_chosen if not question.question_type else None,
        "is_active": question.is_active if not question.question_type else None,
        "step": question.step if question.question_type else None,
        "difficulty": question.difficulty if question.question_type else None,
        "created_at": question.created_at,
        "updated_at": question.updated_at
    }