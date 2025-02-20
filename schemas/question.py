from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionCreate(BaseModel):
    title: str
    question: str
    answer: str
    question_type: Optional[bool] = True  # "테마 문제" 또는 "사용자가 출제한 문제"
    
    # 테마 문제에서만 필요한 필드
    step: Optional[int] = None
    difficulty: Optional[str] = None  # "상", "중", "하"

    # 사용자가 출제한 문제에서만 필요한 필드
    is_approved: Optional[bool] = None
    is_chosen: Optional[bool] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
