from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DiscussionCreate(BaseModel):
    content: str

class DiscussionResponse(BaseModel):
    discussion_id: int
    content: str
    like: int
    comment_exist: bool
    created_date: datetime
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True
