from pydantic import BaseModel

class KakaoLoginRequest(BaseModel):
    code: str
