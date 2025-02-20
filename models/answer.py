from sqlalchemy import Column, BigInteger, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.nolly import Base

class Answer(Base):
    __tablename__ = "answers"

    answer_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)  # 답변 번호
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)  # 사용자 번호
    question_id = Column(BigInteger, ForeignKey("questions.id"), nullable=False)  # 문제 번호 
    content = Column(Text, nullable=False) 

    # 평가 점수
    creativity = Column(Integer, nullable=True)  # 창의 
    logic = Column(Integer, nullable=True)  # 논리 
    thinking = Column(Integer, nullable=True)  # 사고 
    persuasion = Column(Integer, nullable=True)  # 설득 
    depth = Column(Integer, nullable=True)  # 깊이 

    # 평가 근거
    creativity_review = Column(Text, nullable=True)  
    logic_review = Column(Text, nullable=True)  
    thinking_review = Column(Text, nullable=True) 
    persuasion_review = Column(Text, nullable=True) 
    depth_review = Column(Text, nullable=True)  

    # 생성 및 수정 시간
    created_date = Column(DateTime, server_default=func.now(), nullable=False) 
    updated_date = Column(DateTime, onupdate=func.now())  
