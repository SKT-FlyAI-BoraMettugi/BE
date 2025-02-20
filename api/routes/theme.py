from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.theme import get_themes

router = APIRouter()

@router.get('/')
async def get_all_theme(db: Session = Depends(get_db)):
    themes = get_themes(db)
    return themes