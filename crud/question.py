from sqlalchemy.orm import Session
from models.question import Question
from schemas.question import QuestionCreate, QuestionResponse
from datetime import datetime

def save_question(db: Session, user_id: int, question_data: QuestionCreate):
    # 사용자 출제 문제 (False)
    type = question_data.type if question_data.type is not None else False
    
    question = Question(
        user_id=user_id,
        title=question_data.title,
        description=question_data.description,
        answer=question_data.answer,
        type=question_data.type,
    )
    # 테마 문제일 경우
    if question_data.type:
        question.stage = question_data.stage
        question.level = question_data.level

    # 사용자가 출제한 문제일 경우 
    else:
        question.is_approved = False
        question.is_chosen = False
        question.is_active = False
        question.created_at = datetime.utcnow()
        question.updated_at = datetime.utcnow()

    db.add(question)
    db.commit()
    db.refresh(question)
    
    return question

def get_question_detail(db: Session, question_id: int) -> QuestionResponse:
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        return None

    return QuestionResponse(
        type=question.type,
        title=question.title,
        description=question.description,
        answer=question.answer,
        image_url=question.image,
        approval_status=question.approval_status if not question.type else None,
        question_status=question.question_status if not question.type else None,
        now_question=question.now_question if not question.type else None,
        stage=question.stage if question.type else None,
        level=question.level if question.type else None,
        created_date=question.created_date,
        updated_date=question.updated_date
    )