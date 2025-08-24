from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.nolly import Base

class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    discussion_id = Column(BigInteger, nullable=True)
    comment_id = Column(BigInteger, nullable=True)
    content = Column(String(100), nullable=False)
    created_date = Column(DateTime, server_default=func.now())