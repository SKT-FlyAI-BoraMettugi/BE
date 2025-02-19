from sqlalchemy.orm import Session
from models.user import User

def get_user_info(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.user_id == user_id).one()
    return user