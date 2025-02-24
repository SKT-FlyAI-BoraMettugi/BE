from sqlalchemy.orm import Session
from typing import List
from models.user import User
from schemas.nickname import Nickname
from schemas.score import Score
from datetime import datetime

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
    
# 카카오 ID로 유저 조회 
def get_user_by_kakao_id(db: Session, kakao_id: int) -> User:
    return db.query(User).filter(User.kakao_id == kakao_id).first()

# 신규 유저 생성 및 회원가입
def create_user(db: Session, kakao_id: int, nickname: str, profile_image: str, access_token: str) -> User:
    new_user = User(
        character_id=1, 
        nickname=nickname,
        profile_image=profile_image if profile_image else "",
        login_channel="KAKAO",
        kakao_id=kakao_id,  # 카카오 ID 저장
        score=0,
        social_token=access_token,
        updated_date=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
# 카카오 로그인     
def update_kakao_login(db: Session, user_id: int, access_token: str, nickname: str, profile_image: str):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    
    print("db 업데이트 전 access token: ", access_token)
    db_user.social_token = access_token if access_token else "INVALID TOKEN"
    db_user.login_channel = "KAKAO"
    db_user.nickname = nickname
    db_user.profile_image = profile_image
    db_user.updated_date = datetime.utcnow()

    db.commit()
    db.refresh(db_user)
    
    print("db에 저장된 social_token:", db_user.social_token)
    return db_user

# 카카오 로그아웃 
def logout_kakao_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.social_token = ""  # 로그아웃시 초기화
        db.commit()
        db.refresh(user)
