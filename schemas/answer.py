from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnswerResponse(BaseModel):
    answer_content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AnswerScoreResponse(BaseModel):
    creativity: Optional[int] = None
    logic: Optional[int] = None
    thinking: Optional[int] = None
    persuasive: Optional[int] = None
    depth: Optional[int] = None
    creativity_evid: Optional[str] = None
    logic_evid: Optional[str] = None
    thinking_evid: Optional[str] = None
    persuasive_evid: Optional[str] = None
    depth_evid: Optional[str] = None
    total_score: Optional[int] = None  # 총점

    class Config:
        orm_mode = True