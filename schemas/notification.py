from pydantic import BaseModel

class Notification(BaseModel):
    user_id: int
    comment_id: int