from sqlalchemy.orm import Session
from models.discussion import Discussion, DiscussionLike
from schemas.discussion import DiscussionCreate, DiscussionLikeResponse
from typing import List

def create_discussion(db: Session, user_id: int, question_id: int, discussion_data: DiscussionCreate):
    new_discussion = Discussion(
        user_id=user_id,
        question_id=question_id,
        content=discussion_data.content
    )
    db.add(new_discussion)
    db.commit()
    db.refresh(new_discussion)
    return new_discussion

def get_discussions_by_question(db: Session, question_id: int):
    return db.query(Discussion).filter(Discussion.question_id == question_id).all()

# 토론 좋아요 추가
def add_like_to_discussion(db: Session, discussion_id: int, user_id: int):
    discussion = db.query(Discussion).filter(Discussion.discussion_id == discussion_id).first()
    
    # 사용자가 이미 좋아요를 눌렀는지 확인
    existing_like = db.query(DiscussionLike).filter(
        DiscussionLike.discussion_id == discussion_id,
        DiscussionLike.user_id == user_id
    ).first()

    if existing_like:
        # 이미 눌렀다면 삭제 (좋아요 취소)
        db.delete(existing_like)
        discussion.like -= 1
        liked = False
    else:
        # 좋아요 추가
        new_like = DiscussionLike(discussion_id=discussion_id, user_id=user_id)
        db.add(new_like)
        discussion.like += 1
        liked = True

    db.commit()
    db.refresh(discussion)

    return {"discussion_id": discussion_id, "like": discussion.like, "liked": liked}

# 좋아요 누른 토론 조회
def get_liked_discussions_by_user(db: Session, user_id: int) -> List[Discussion]:
    return db.query(Discussion).join(DiscussionLike, Discussion.discussion_id == DiscussionLike.discussion_id)\
        .filter(DiscussionLike.user_id == user_id).all()