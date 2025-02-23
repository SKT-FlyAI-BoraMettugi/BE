from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.user import get_user_info, update_user_nickname, update_kakao_login, logout_kakao_user
from schemas.nickname import Nickname
from schemas.login import KakaoLoginRequest
from core.kakao_api import KakaoAPI

router = APIRouter()
kakao_api = KakaoAPI()

@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_info(user_id, db)
    return user

@router.patch('/nickname/{user_id}')
async def update_nickname(nickname: Nickname, db: Session = Depends(get_db)):
    update_user_nickname(nickname, db)
    return nickname

# user 생성 

# 카카오 로그인 url 반환
@router.get("/auth/kakao/login-url")
def get_kakao_login_url():
    return {"login_url": kakao_api.get_auth_url()}

# 카카오 로그인 후 받은 code를 JSON으로 반환
@router.get("/auth/kakao/callback")
async def kakao_callback(code: str):
    return {"code": code}

# 프론트에서 code 보냄
@router.patch("/login/{user_id}")
async def kakao_login(user_id: int, request: KakaoLoginRequest, db: Session = Depends(get_db)):
    
    # 인가 코드로 카카오에서 액세스 토큰 요청
    token_data = await kakao_api.get_access_token(request.code)
    access_token = token_data.get("access_token")
    print(" 액세스 토큰:", access_token)

    if not access_token:
        raise HTTPException(status_code=400, detail="카카오 액세스 토큰 발급 실패")

    # 액세스 토큰으로 사용자 정보 요청
    user_data = await kakao_api.get_user_info(access_token)
    kakao_id = user_data["id"]
    nickname = user_data["kakao_account"]["profile"].get("nickname", "No Nickname")
    profile_image = user_data["kakao_account"]["profile"].get("profile_image_url", None)
    print("저장할 닉네임: ", nickname)
    
    # DB 업데이트 수행
    db_user = update_kakao_login(db, user_id, access_token, nickname, profile_image)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "카카오 로그인 성공", "user_id": user_id, "nickname": nickname}

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
