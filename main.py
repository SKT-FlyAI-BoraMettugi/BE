import uvicorn
from fastapi import FastAPI
from api import main
from starlette.middleware.cors import CORSMiddleware
from core.minio_service import download_model_from_minio # 모델 파일 다운로드
from core.model_loader import load_model # load_tokenizer, tokenizer, 모델 로드
from database.redis import redis_client

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.api_router)

@app.on_event("startup")
async def startup_redis():
    app.state.redis = redis_client

@app.on_event("shutdown")
async def shutdown_redis():
    await app.state.redis.close()

# 서버 실행 시 모델 파일 다운로드 + 모델 로드
@app.on_event("startup")
async def cache_model():
    download_model_from_minio(f"models", "downloaded_model") # MODEL_PATH : 어제 test 시 "test_download" 사용
    app.state.model, app.state.tokenizer = load_model()

#if __name__ == '__main__':
    #uvicorn.run('main:app', reload=True)
