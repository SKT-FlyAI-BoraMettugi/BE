from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnswerResponse(BaseModel):
    content: str
    created_date: datetime
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class AnswerScoreResponse(BaseModel):
    creativity: Optional[int] = None
    logic: Optional[int] = None
    thinking: Optional[int] = None
    persuasion: Optional[int] = None
    depth: Optional[int] = None
    creativity_review: Optional[str] = None
    logic_review: Optional[str] = None
    thinking_review: Optional[str] = None
    persuasion_review: Optional[str] = None
    depth_review: Optional[str] = None
    total_score: Optional[int] = None  # 총점

    class Config:
        orm_mode = True