from sqlalchemy import Column, BigInteger, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.nolly import Base

class Discussion(Base):
    __tablename__ = "discussions"

    discussion_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    question_id = Column(BigInteger, ForeignKey("questions.question_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    like = Column(Integer, default=0, nullable=False)
    comment_exist = Column(Boolean, default=False, nullable=False)
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    updated_date = Column(DateTime, onupdate=func.now(), nullable=True)

class DiscussionLike(Base):
    __tablename__ = "discussion_likes"

    discussion_likes_id = Column(BigInteger, primary_key=True, autoincrement=True)
    discussion_id = Column(BigInteger, ForeignKey("discussions.discussion_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)