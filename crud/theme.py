from sqlalchemy.orm import Session
from typing import List
from models.theme import Theme
from schemas.theme_list import Theme_list
from schemas.theme_per import Theme_per

# 전체 테마 조회
def get_themes(db: Session) -> List[Theme_list]:

    themes = db.query( # themes: List[tuple] 형태
        Theme.theme_id,
        Theme.theme_name,
        Theme.theme_ex, # None 허용
        Theme.profile_img
    ).all()
    
    return [ # 튜플을 ThemeList로 변환
        Theme_list(
            theme_id=row[0],
            theme_name=row[1],
            theme_ex=row[2],
            profile_img=row[3]
        )
        for row in themes
    ] 

# return 형태
# [
#     ThemeList(theme_id=1, theme_name='공룡', theme_ex='공룡 테마 설명', profile_img='profile.png'),
#     ThemeList(theme_id=2, theme_name='용암', theme_ex='용암 테마 설명', profile_img='lava.png')
# ]

# 테마 별 페이지 조회
def get_per_theme(theme_id: int, db:Session) -> List[Theme_per]:
    pass
