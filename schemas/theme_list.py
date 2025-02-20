from pydantic import BaseModel
from typing import Optional

class Theme_list(BaseModel):
    theme_id: int
    theme_name: str
    theme_ex: Optional[str]
    profile_img: str