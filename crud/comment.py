from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate
from datetime import datetime
from typing import List

# 답글 달기 
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

# 답글 좋아요
def add_like_to_comment(db: Session, comment_id: int, user_id: int):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()

    if not comment:
        return None  # 댓글이 존재하지 않음

    # 좋아요 토글: 0이면 +1, 1 이상이면 -1
    if comment.like == 0:
        comment.like += 1  # 좋아요 추가
    else:
        comment.like -= 1  # 좋아요 취소

    db.commit()
    db.refresh(comment)

    return comment

# 사용자가 좋아요 누른 답글 조회
def get_liked_comments_by_user(db: Session, user_id: int):
    return db.query(Comment).filter(Comment.user_id == user_id, Comment.like > 0).all()

# 토론에 대한 모든 답글 조회
def get_comments_by_discussion_id(db: Session, discussion_id: int) -> List[Comment]:
    return db.query(Comment).filter(Comment.discussion_id == discussion_id).all()