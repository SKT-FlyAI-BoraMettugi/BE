from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from core.ranking import calculate_ranking
from crud.user import get_all_users_score

router = APIRouter()

@router.get('/')
async def get_all_ranking(db: Session = Depends(get_db)):
    scores = get_all_users_score(db)
    rankings = calculate_ranking(scores)
    return rankings