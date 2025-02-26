from pydantic import BaseModel

class KakaoLoginRequest(BaseModel):
    kakao_id: int
    nickname: str
    profile_img: str
