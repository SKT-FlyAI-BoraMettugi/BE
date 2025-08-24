from pydantic import BaseModel
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: int
    discussion_id: Optional[int]
    comment_id: Optional[int]
    content: str