from sqlalchemy import Column, BigInteger, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.nolly import Base

class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    discussion_id = Column(BigInteger, ForeignKey("discussions.discussion_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    like = Column(Integer, default=0, nullable=False)
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    updated_date = Column(DateTime, onupdate=func.now(), nullable=True)

class CommentLike(Base):
    __tablename__ = "comment_likes"

    comment_likes_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    comment_id = Column(BigInteger, ForeignKey("comments.comment_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)