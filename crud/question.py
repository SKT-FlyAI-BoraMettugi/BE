from sqlalchemy.orm import Session
from models.question import Question
from schemas.question import QuestionCreate
from datetime import datetime

def save_question(db: Session, user_id: int, question_data: QuestionCreate):
    question = Question(
        user_id=user_id,
        title=question_data.title,
        question=question_data.question,
        answer=question_data.answer,
        question_type=question_data.question_type,
    )

    # 테마 문제일 경우 step, difficulty 저장
    if question_data.question_type == "테마 문제":
        question.step = question_data.step
        question.difficulty = question_data.difficulty

    # 사용자가 출제한 문제일 경우 is_approved, is_chosen, is_active, created_at, updated_at 저장
    elif question_data.question_type == "사용자가 출제한 문제":
        question.is_approved = False
        question.is_chosen = False
        question.is_active = False
        question.created_at = datetime.utcnow()
        question.updated_at = datetime.utcnow()

    db.add(question)
    db.commit()
    db.refresh(question)
    return question
