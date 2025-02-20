from sqlalchemy.orm import Session
from typing import List
from models.theme import Theme
from schemas.theme_list import Theme_list
from schemas.theme_per import Theme_per
from models.question import Question

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
#     Theme_list(theme_id=1, theme_name='공룡', theme_ex='공룡 테마 설명', profile_img='profile.png'),
#     Theme_list(theme_id=2, theme_name='용암', theme_ex='용암 테마 설명', profile_img='lava.png')
# ]

# 테마 별 페이지 조회

def get_per_theme(theme_id: int, user_id: int, db:Session) -> List[Theme_per]:
    # output == Theme_per / 테마>문제 별 색상 지정해야 함.
    
    # 1. 테마에 해당하는 "문제" 전체 listup
    # 2. "문제" 번호 순서대로 sort
    questions = db.query(
        Question.theme_id, # 테마 번호
        Question.user_id, # 사용자 번호
        Question.stage # 테마 내 문제 번호
    )\
    .filter(Question.theme_id == theme_id)\
    .order_by(Question.stage.asc())\
    .all()

    # 3. "답변" db와 비교해 사용자가 몇 번 문제까지 풀었는지 확인
    '''
    theme_color 구현 예정~!~
    '''

    return [
        Theme_per(
            theme_id=row[0],
            user_id=row[1],
            stage=row[2]
        )
        for row in questions # theme_color
    ]
