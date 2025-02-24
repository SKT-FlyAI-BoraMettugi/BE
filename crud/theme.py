from sqlalchemy.orm import Session
from typing import List
from models.theme import Theme
from schemas.theme import Theme_list, Theme_per
from models.question import Question
from models.answer import Answer

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

def get_per_theme(theme_id: int, user_id: int, db: Session) -> List[Theme_per]:
    """
    1) theme_id에 해당하는 Theme 정보를 조회
    2) questions에서 theme_id 일치하는 문제를 stage ASC 정렬로 조회
    3) answers에서 (user_id 일치)인 답변 리스트를 가져와, question별 '최고 점수'를 구한다.
       → 최고 점수가 35 이상이면 해당 question은 solved.
    4) stage 범위(1~4, 5~8, 9~12)에 따라 succ/fail 색상 분기
    5) Theme_per 리스트로 반환
    """

    # 1) Theme 정보 가져오기
    theme = db.query(Theme).filter(Theme.theme_id == theme_id).one_or_none()
    if not theme:
        return []

    # 2) 문제 리스트(stage ASC)
    questions = (
        db.query(Question)
        .filter(Question.theme_id == theme_id)
        .order_by(Question.stage.asc())
        .all()
    )

    # 3) 답변: question_id별 최대 점수 계산
    #    한 문제에 대해 여러 답변이 있으면, 그 중 하나라도 35점 이상이면 solved
    answers = db.query(Answer).filter(Answer.user_id == user_id).all()

    # 딕셔너리: { question_id: max_score }
    max_score_map = {}
    for ans in answers:
        total_score = (
            (ans.creativity or 0) +
            (ans.logic or 0) +
            (ans.thinking or 0) +
            (ans.persuasion or 0) +
            (ans.depth or 0)
        )
        if ans.question_id not in max_score_map:
            max_score_map[ans.question_id] = total_score
        else:
            # 더 높은 점수가 있으면 갱신
            if total_score > max_score_map[ans.question_id]:
                max_score_map[ans.question_id] = total_score

    # solved 여부: max_score_map[q_id] >= 35
    solved_questions = {
        q_id
        for q_id, score in max_score_map.items()
        if score >= 35
    }

    # 4) stage 범위 + solved 여부 색상 분기
    result_list = []
    for q in questions:
        stage_val = q.stage or 0
        is_solved = (q.question_id in solved_questions)

        # 색상 필드 초기화
        high_succ_color = None
        high_fail_color = None
        mid_succ_color = None
        mid_fail_color = None
        low_succ_color = None
        low_fail_color = None

        if 1 <= stage_val <= 4:
            # 하 난이도
            if is_solved:
                low_succ_color = theme.low_succ_color
            else:
                low_fail_color = theme.low_fail_color
        elif 5 <= stage_val <= 8:
            # 중 난이도
            if is_solved:
                mid_succ_color = theme.mid_succ_color
            else:
                mid_fail_color = theme.mid_fail_color
        elif 9 <= stage_val <= 12:
            # 상 난이도
            if is_solved:
                high_succ_color = theme.high_succ_color
            else:
                high_fail_color = theme.high_fail_color

        # 5) Theme_per 스키마 구성
        item = Theme_per(
            theme_id=q.theme_id,
            user_id=user_id,
            stage=stage_val,

            theme_name=theme.theme_name,
            background_img=theme.background_img,

            high_succ_color=high_succ_color,
            high_fail_color=high_fail_color,
            mid_succ_color=mid_succ_color,
            mid_fail_color=mid_fail_color,
            low_succ_color=low_succ_color,
            low_fail_color=low_fail_color,
        )
        result_list.append(item)

    return result_list
