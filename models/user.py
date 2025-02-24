import enum
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Enum
from sqlalchemy.sql import func
from database.nolly import Base

class LoginChannel(enum.Enum):
    KAKAO = "KAKAO"
    NAVER = "NAVER"
    T = "T"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, nullable=False)
    nickname = Column(String(10), nullable=False)
    profile_image = Column(String(100), nullable=True)
    login_channel = Column(Enum(LoginChannel), nullable=True)
    kakao_id = Column(BigInteger, unique=True, nullable=False)
    score = Column(Integer, nullable=False)
    social_token = Column(String(255), nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, onupdate=func.now())