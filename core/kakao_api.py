import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(override=True)

class KakaoAPI:
    def __init__(self):
        self.client_id = os.getenv("KAKAO_CLIENT_ID")
        self.redirect_uri =os.getenv("KAKAO_REDIRECT_URI")
        self.kakao_auth_url = "https://kauth.kakao.com/oauth/authorize"
        self.kakao_token_url = "https://kauth.kakao.com/oauth/token"
        self.kakao_user_info_url = "https://kapi.kakao.com/v2/user/me"

    # 카카오 로그인 url 생성 
    def get_auth_url(self):
        return {
             f"{self.kakao_auth_url}?response_type=code"
             f"&client_id={self.client_id}"
             f"&redirect_uri={self.redirect_uri}"
        }
    # 인가 코드로 액세스 토큰 요청
    async def get_access_token(self, code: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.kakao_token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "redirect_uri": self.redirect_uri,
                    "code": code,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        # 🔹 카카오 API 응답 로그 출력
        print("카카오 토큰 응답:", response.json())

        # ✅ HTTP 상태 코드 체크 추가 (잘못된 응답 처리)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"카카오 액세스 토큰 요청 실패: {response.text}")

        return response.json()

    # 액세스 토큰으로 사용자 정보 요청
    async def get_user_info(self, access_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.kakao_user_info_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        return response.json()
    
    # 카카오 로그아웃 
    async def logout_user(self, access_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://kapi.kakao.com/v1/user/logout",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return response.json()