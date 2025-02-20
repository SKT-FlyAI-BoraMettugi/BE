from sqlalchemy.orm import Session
from models.answer import Answer

def get_answer_history(db: Session, user_id: int, question_id: int):
    return db.query(Answer).filter(Answer.user_id == user_id, Answer.question_id == question_id).all()

def get_answer_scores(db: Session, user_id: int, question_id: int):
    answer = db.query(
        Answer.creativity, 
        Answer.logic, 
        Answer.thinking, 
        Answer.persuasion, 
        Answer.depth,
        Answer.creativity_review, 
        Answer.logic_review, 
        Answer.thinking_review, 
        Answer.persuasion_review, 
        Answer.depth_review
    ).filter(
        Answer.user_id == user_id,
        Answer.question_id == question_id
    ).first()

    if answer: # 총점 합산 로직
        total_score = sum(filter(None, [answer.creativity, answer.logic, answer.thinking, answer.persuasion, answer.depth]))  # None 값 방지
        return {
            **answer._asdict(),
            "total_score": total_score
        }
    return None