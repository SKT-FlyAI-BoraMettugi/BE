from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate
from datetime import datetime

def create_comment(db: Session, user_id: int, discussion_id: int, comment_data: CommentCreate):
    new_comment = Comment(
        user_id=user_id,
        discussion_id=discussion_id,
        content=comment_data.content,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
