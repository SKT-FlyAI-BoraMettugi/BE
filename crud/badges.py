from sqlalchemy.orm import Session
from typing import Optional
from models.badges import Badges
from schemas.badges import BadgeCreate, BadgeResponse, BadgeUpdate
from models.question import Question
from models.answer import Answer
from models.theme import Theme

def get_badges(db: Session, user_id: int, theme_id: int) -> Optional[Badges]:
    """
    특정 유저(user_id)와 테마(theme_id)에 대한 배지(Badges) 정보
    없다면 None 반환.
    """
    return db.query(Badges).filter(
        Badges.user_id == user_id,
        Badges.theme_id == theme_id
    ).first()

def find_badges_grade(user_id: int, theme_id: int, db: Session) -> Optional[str]:
    '''
    특정 유저, 테마에 대한 배지의 grade를 조회, 문자열 반환
    '''
    row = (
        db.query(Badges.grade)
        .filter(Badges.user_id == user_id, Badges.theme_id == theme_id)
        .one_or_none()
    )
    if row is not None:
        return row[0]
    return None


def update_badges(user_id: int, theme_id: int, db: Session) -> BadgeResponse:
    '''
    PATCH
    1) 유저가 이 테마에서 몇 문제 풀었는지 계산
    2) 풀었으면 동(>=4), 은(>=8), 금(>=12) 등급 설정
    3) Badges 테이블에 없으면 생성, 있으면 업데이트
    4) 최종 결과 반환
    '''

    # 1) 유저가 이 테마에서 몇 문제 풀었는지 계산
    questions = (
        db.query(Question)
        .filter(Question.theme_id == theme_id)
        .all()
    )
    answers = (
        db.query(Answer)
        .filter(Answer.user_id == user_id)
        .all()
    )
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
            if total_score > max_score_map[ans.question_id]:
                max_score_map[ans.question_id] = total_score

    # 풀었는지 여부 (35 이상)
    solved_count = 0
    for q in questions:
        if q.question_id in max_score_map and max_score_map[q.question_id] >= 35:
            solved_count += 1

    # 2) solved_count 기반으로 배지 등급 결정
    new_grade = None
    if solved_count >= 12:
        new_grade = "금"
    elif solved_count >= 8:
        new_grade = "은"
    elif solved_count >= 4:
        new_grade = "동"
    # else: new_grade = None (미획득 상태)

    # 3) Badges 테이블에서 기존 레코드 조회 (없으면 생성)
    existing_badge = get_badges(db, user_id, theme_id)
    if existing_badge:
        # 이미 있으면 업데이트
        existing_badge.grade = new_grade
        db.commit()
        db.refresh(existing_badge)
        updated_badge = existing_badge
    else:
        # 없으면 새로 생성
        new_badge = Badges(
            user_id=user_id,
            theme_id=theme_id,
            grade=new_grade
        )
        db.add(new_badge)
        db.commit()
        db.refresh(new_badge)
        updated_badge = new_badge

    # 4) 스키마 변환
    return BadgeResponse(
        badges_id=updated_badge.badges_id,
        user_id=updated_badge.user_id,
        theme_id=updated_badge.theme_id,
        grade=updated_badge.grade
    )