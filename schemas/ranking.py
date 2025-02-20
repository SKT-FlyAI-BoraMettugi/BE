from pydantic import BaseModel

class Ranking(BaseModel):
    user_id: int
    score: int
    rank: int