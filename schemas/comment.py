from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    user_id: int
    comment_id: int
    content: str
    like: int
    created_date: datetime
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class CommentLikeResponse(BaseModel):
    like: int

    class Config:
        orm_mode = True