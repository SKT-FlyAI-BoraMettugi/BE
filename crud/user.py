from sqlalchemy.orm import Session
from typing import List
from models.user import User
from schemas.nickname import Nickname
from schemas.score import Score

def get_user_info(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.user_id == user_id).one()
    return user

def get_all_users_score(db: Session) -> List[Score]:
    users = db.query(User.user_id, User.score).all()
    scores = [Score(user_id=user.user_id, score=user.score) for user in users]
    return scores

def update_user_score(score: Score, db: Session) -> None:
    db.query(User).filter(User.user_id == score.user_id).update({"score": score.score})
    db.commit()

def update_user_nickname(nickname: Nickname, db: Session) -> None:
    db.query(User).filter(User.user_id == nickname.user_id).update({"nickname": nickname.nickname})
    db.commit()