from sqlalchemy.orm import Session
from models.discussion import Discussion
from schemas.discussion import DiscussionCreate, DiscussionLikeResponse

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

# 토론 좋아요 
def add_like_to_discussion(db: Session, discussion_id: int, user_id: int):
    discussion = discussion = db.query(Discussion).filter(Discussion.discussion_id == discussion_id).first()
    # 좋아요 토글: 좋아요가 1 이상이면 취소, 0이면 추가
    if discussion.like > 0:
        discussion.like -= 1  # 좋아요 취소
        liked = False
    else:
        discussion.like += 1  # 좋아요 추가
        liked = True

    db.commit()
    db.refresh(discussion)

    return {"discussion_id": discussion_id, "like": discussion.like, "liked": liked}    