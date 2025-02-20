from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnswerResponse(BaseModel):
    answer_content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
