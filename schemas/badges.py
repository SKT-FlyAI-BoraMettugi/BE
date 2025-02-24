from pydantic import BaseModel
from typing import Optional

# badge table에 기본적으로 들어가는 필드 정의
class BadgeBase(BaseModel):
    user_id: int
    theme_id: int

# badge 새로 정의할 때 필요한 필드
class BadgeCreate(BadgeBase):
    grade: Optional[str] = None # 금, 은, 동

# badge 정보 조회 시 반환되는 스키마
class BadgeResponse(BadgeBase):
    badges_id: int
    grade: Optional[str] = None

# PATCH로 grade만 업데이트할 때 사용
class BadgeUpdate(BaseModel):
    grade: Optional[str] = None