from pydantic import BaseModel

class Theme_per(BaseModel):
    theme_id: int
    theme_name: str

    background_img: str

    high_succ_color: str
    high_fail_color: str

    mid_succ_color: str
    mid_fail_color: str

    low_succ_color: str
    low_fail_color: str