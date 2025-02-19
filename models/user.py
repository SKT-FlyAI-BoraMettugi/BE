import enum
from sqlalchemy import Column, String, Integer, DateTime, Enum
from database.nolly import Base

class LoginChannel(enum.Enum):
    KAKAO = "KAKAO"
    NAVER = "NAVER"
    T = "T"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, nullable=False)
    nickname = Column(String, nullable=False)
    profile_image = Column(String, nullable=True)
    login_channel = Column(Enum(LoginChannel), nullable=False)
    score = Column(Integer, nullable=False)
    social_token = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)