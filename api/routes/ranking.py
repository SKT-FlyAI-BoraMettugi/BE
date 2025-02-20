from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from core.ranking import calculate_ranking, calculate_user_ranking
from crud.user import get_all_users_score, update_user_score
from schemas.score import Score

router = APIRouter()

@router.get('/')
async def get_all_ranking(db: Session = Depends(get_db)):
    scores = get_all_users_score(db)
    rankings = calculate_ranking(scores)
    return rankings

@router.get('/{user_id}')
async def get_ranking(user_id: int, db: Session = Depends(get_db)):
    scores = get_all_users_score(db)
    ranking = calculate_user_ranking(scores, user_id)
    return ranking

@router.patch('/{user_id}')
async def update_score(score: Score, db: Session = Depends(get_db)):
    update_user_score(score, db)
    return score