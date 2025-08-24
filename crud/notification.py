from sqlalchemy.orm import Session
from datetime import datetime
from models.notification import Notification
from schemas.notification import NotificationCreate

# 알림 생성
def create_notification(db: Session, notification_data: NotificationCreate):
    notification = Notification(
        user_id=notification_data.user_id,
        discussion_id=notification_data.discussion_id,
        comment_id=notification_data.comment_id,
        content=notification_data.content,
        created_date=datetime.utcnow(),
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

# 유저 알림 조회
def get_notification(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_date.desc()).all()
