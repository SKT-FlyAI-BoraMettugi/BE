from sqlalchemy.orm import Session
from typing import List
from models.user import User
from schemas.score import Score

def get_user_info(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.user_id == user_id).one()
    return user

def get_all_users_score(db: Session) -> List[Score]:
    users = db.query(User.user_id, User.score).all()
    scores = [Score(user_id=user.user_id, score=user.score) for user in users]
    return scores