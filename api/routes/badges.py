from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.badges import find_badges_grade, update_badges

router = APIRouter()

# 뱃지 등급 조회
@router.get("/{user_id}/{theme_id}")
async def get_badge_grade(user_id: int, theme_id: int, db: Session = Depends(get_db)):
    badge_grade = find_badges_grade(user_id, theme_id, db)
    return badge_grade

# 뱃지 등급 업데이트
@router.patch("/{user_id}/{theme_id}")
async def update_badge_grade(user_id: int, theme_id: int, db: Session = Depends(get_db)):
    """
    특정 user_id와 theme_id에 대해, 풀었는지 체크 후 등급 계산 → badges 테이블에 반영
    """
    updated_badge_grade = update_badges(user_id, theme_id, db)
    return updated_badge_grade
