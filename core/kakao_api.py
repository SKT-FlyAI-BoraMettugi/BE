import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class KakaoAPI:
    def __init__(self):
        self.client_id = os.getenv("KAKAO_CLIENT_ID")
        self.redirect_uri =os.getenv("KAKAO_REDIRECT_URI")
        self.kakao_auth_url = "https://kauth.kakao.com/oauth/authorize"
        self.kakao_token_url = "https://kauth.kakao.com/oauth/token"
        self.kakao_user_info_url = "https://kapi.kakao.com/v2/user/me"

    # 카카오 로그아웃 
    async def logout_user(self, access_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://kapi.kakao.com/v1/user/logout",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return response.json()