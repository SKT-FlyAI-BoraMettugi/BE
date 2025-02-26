from sqlalchemy.orm import Session
from models.comment import Comment, CommentLike
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

    # 사용자가 이미 좋아요를 눌렀는지 확인
    existing_like = db.query(CommentLike).filter(
        CommentLike.comment_id == comment_id,
        CommentLike.user_id == user_id
    ).first()

    if existing_like:
        # 이미 눌렀다면 삭제 (좋아요 취소)
        db.delete(existing_like)
        comment.like -= 1
        liked = False
    else:
        # 좋아요 추가
        new_like = CommentLike(comment_id=comment_id, user_id=user_id)
        db.add(new_like)
        comment.like += 1
        liked = True

    db.commit()
    db.refresh(comment)

    return {"comment_id": comment_id, "like": comment.like, "liked": liked}

# 사용자가 좋아요 누른 답글 조회
def get_liked_comments_by_user(db: Session, user_id: int):
    return db.query(Comment).join(CommentLike, Comment.comment_id == CommentLike.comment_id)\
        .filter(CommentLike.user_id == user_id).all()

# 토론에 대한 모든 답글 조회
def get_comments_by_discussion_id(db: Session, discussion_id: int) -> List[Comment]:
    return db.query(Comment).filter(Comment.discussion_id == discussion_id).all()