from sqlalchemy.orm import Session
from models.answer import Answer

def get_answer_history(db: Session, user_id: int, question_id: int):
    return db.query(Answer).filter(Answer.user_id == user_id, Answer.question_id == question_id).all()


def get_answer_scores(db: Session, user_id: int, question_id: int):
    answer = db.query(
        Answer.creativity, 
        Answer.logic, 
        Answer.thinking, 
        Answer.persuasive, 
        Answer.depth,
        Answer.creativity_evid, 
        Answer.logic_evid, 
        Answer.thinking_evid, 
        Answer.persuasive_evid, 
        Answer.depth_evid
    ).filter(
        Answer.user_id == user_id,
        Answer.question_id == question_id
    ).first()

    if answer: # 총점 합산 로직
        total_score = sum(filter(None, [answer.creativity, answer.logic, answer.thinking, answer.persuasive, answer.depth]))  # None 값 방지
        return {
            **answer._asdict(),
            "total_score": total_score
        }
    return None