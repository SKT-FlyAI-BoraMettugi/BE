from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.user import get_user_info, update_user_nickname, get_user_by_kakao_id, create_user, update_kakao_login, logout_kakao_user, get_all_users
from schemas.nickname import Nickname
from schemas.login import KakaoLoginRequest
from schemas.user import UserResponse
from typing import List
from core.kakao_api import KakaoAPI
import random

router = APIRouter()
kakao_api = KakaoAPI()

# 전체 유저 조회
@router.get("/all", response_model=List[UserResponse])
async def get_all_users_api(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_info(user_id, db)
    return user

@router.patch('/nickname/{user_id}')
async def update_nickname(nickname: Nickname, db: Session = Depends(get_db)):
    update_user_nickname(nickname, db)
    return nickname

# 카카오 로그인 url 반환
@router.get("/auth/kakao/login-url")
def get_kakao_login_url():
    return {"login_url": kakao_api.get_auth_url()}

# 카카오 로그인 후 받은 code를 JSON으로 반환
@router.get("/auth/kakao/callback")
async def kakao_callback(code: str):
    return {"code": code}

# 프론트에서 code 보냄
@router.patch("/login")
async def kakao_login(request: KakaoLoginRequest, db: Session = Depends(get_db)):
    kakao_id = request.kakao_id
    nickname = request.nickname
    profile_image = request.profile_img

    # DB에서 기존 유저 확인
    user = get_user_by_kakao_id(db, kakao_id)

    if user:
        # 기존 유저: 로그인 처리 
        update_kakao_login(db, user.user_id, None, nickname, profile_image)
        return {"message": "카카오 로그인 성공", "user_id": user.user_id, "nickname": nickname}

    # 신규 유저: 회원가입 후 로그인 처리
    new_user = create_user(db, kakao_id, nickname, profile_image, None)

    return {"message": "회원가입 및 로그인 성공", "user_id": new_user.user_id, "nickname": nickname}

# 카카오 로그아웃
@router.patch("/logout/{user_id}")
async def kakao_logout(user_id: int, db: Session = Depends(get_db)):
    # 사용자 정보 조회
    user = get_user_info(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 카카오 액세스 토큰 확인
    access_token = user.social_token
    if not access_token:
        raise HTTPException(status_code=400, detail="이미 로그아웃된 사용자입니다.")

    # 카카오 로그아웃 API 호출
    logout_response = await kakao_api.logout_user(access_token)
    if not logout_response.get("id"):
        raise HTTPException(status_code=400, detail="카카오 로그아웃 실패")

    # DB에서 `social_token` 초기화 
    logout_kakao_user(db, user_id)

    return {"message": "카카오 로그아웃 성공", "user_id": user_id}
