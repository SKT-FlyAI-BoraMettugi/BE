from pydantic import BaseModel

class Nickname(BaseModel):
    user_id: int
    nickname: str