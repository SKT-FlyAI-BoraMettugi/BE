from sqlalchemy.orm import Session
from models.answer import Answer

def get_answer_history(db: Session, user_id: int, question_id: int):
    return db.query(Answer).filter(Answer.user_id == user_id, Answer.question_id == question_id).all()
