from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.theme import get_themes, get_per_theme

router = APIRouter()

@router.get('/')
async def get_all_theme(db: Session = Depends(get_db)):
    themes = get_themes(db)
    return themes

@router.get('/{theme_id}/{user_id}')
async def get_theme_color(theme_id: int, user_id: int, db:Session = Depends(get_db)):
    themes_color = get_per_theme(user_id, theme_id, db)
    return themes_color