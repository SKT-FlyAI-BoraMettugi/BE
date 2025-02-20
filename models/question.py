from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.nolly import Base

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)  # 문제 번호 
    theme_id = Column(BigInteger, ForeignKey("themes.id"), nullable=True)  # 테마 번호 
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=True)  # 사용자 번호 
    type = Column(Boolean, nullable = False, default = True) # 문제 종류
    title = Column(String(50), nullable=False)  # 문제 제목
    description = Column(Text, nullable=False)  # 문제 설명
    answer = Column(Text, nullable= True)  # 출제자가 생각한 정답
    image = Column(String(100), nullable=True)  # 문제 이미지 URL
    approval_status = Column(Boolean, default=False)  # 관리자 승인 여부
    question_status = Column(Boolean, default=False)  # 이 주의 문제 채택 여부
    now_question = Column(Boolean, default=False)  # 현재 출제 중 여부
    stage = Column(Integer, nullable=True)  # 테마 내 문제 번호
    level = Column(Enum("상", "중", "하", name="difficulty_enum"), nullable=True)  # 문제 난이도
    created_date = Column(DateTime, server_default=func.now())  # 문제 생성 시간
    updated_date = Column(DateTime, onupdate=func.now())  # 문제 수정 시간
