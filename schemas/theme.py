from pydantic import BaseModel
from typing import Optional

class Theme_list(BaseModel):
    theme_id: int
    theme_name: str
    theme_ex: Optional[str]
    profile_img: str
    background_img: str

class Theme_per(BaseModel):
    theme_id: int
    user_id: int
    stage: int
    question_id: int
    theme_name: str

    # 1~4
    high_succ_color: Optional[str] = None
    high_fail_color: Optional[str] = None

    # 5~8
    mid_succ_color: Optional[str] = None
    mid_fail_color: Optional[str] = None

    # 9~12
    low_succ_color: Optional[str] = None
    low_fail_color: Optional[str] = None
    