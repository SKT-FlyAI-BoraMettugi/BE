from sqlalchemy.orm import Session
from models.discussion import Discussion
from schemas.discussion import DiscussionCreate

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
