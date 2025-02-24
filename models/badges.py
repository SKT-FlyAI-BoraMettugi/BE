from sqlalchemy import Column, BigInteger, Text, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from database.nolly import Base

class Badges(Base):
    __tablename__ = "badges"
    
    badges_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False) # 배지 번호
    user_id = Column(BigInteger, ForeignKey("users.user_id"), autoincrement=True, nullable=False) # 사용자 번호
    theme_id = Column(BigInteger, ForeignKey("theme.theme_id"), autoincrement=True, nullable=False) # 테마 번호

    grade = Column(Enum("금","은","동", name="badge_grade"), nullable=True) # 배지 등급
    created_date = Column(DateTime, server_default=func.now()) # 배지 생성 시간
    updated_date = Column(DateTime, onupdate=func.now()) # 배지 수정 시간