from pydantic import BaseModel

class Score(BaseModel):
    user_id: int
    score: int