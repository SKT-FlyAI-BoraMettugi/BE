from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionCreate(BaseModel):
    title: str
    description: str
    answer: str
    type: Optional[bool] = True  # "테마 문제" 또는 "사용자가 출제한 문제"
    
    # 테마 문제에서만 필요한 필드
    theme_id: Optional[int] = None
    stage: Optional[int] = None
    level: Optional[str] = None  # "상", "중", "하"

    # 사용자가 출제한 문제에서만 필요한 필드
    approval_status: Optional[bool] = None
    question_status: Optional[bool] = None
    now_question: Optional[bool] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

class QuestionResponse(BaseModel):
    type: bool
    title: str
    description: str
    theme_id:  Optional[int] = None
    answer: Optional[str]
    image_url: Optional[str]
    approval_status: Optional[bool] = None
    question_status: Optional[bool] = None
    now_question: Optional[bool] = None
    stage: Optional[int] = None
    level: Optional[str] = None
    created_date: datetime
    updated_date: Optional[datetime]