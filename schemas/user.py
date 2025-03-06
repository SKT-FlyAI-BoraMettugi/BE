from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.user import LoginChannel  

class UserResponse(BaseModel):
    user_id: int
    character_id: int
    nickname: str
    profile_image: Optional[str]
    login_channel: Optional[LoginChannel]  
    kakao_id: int
    score: int
    created_date: datetime = None
    updated_date: Optional[datetime] = None

    class Config:
        orm_mode = True  
