import uvicorn
from fastapi import FastAPI
from api import main
from starlette.middleware.cors import CORSMiddleware
from core.redis_subscriber import start_redis_subscriber
from core.minio_service import download_model_from_minio # 모델 파일 다운로드
from core.model_loader import load_model # load_tokenizer, tokenizer, 모델 로드
import os

# import torch

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

# 서버 실행 시 모델 파일 다운로드 + 모델 로드
@app.on_event("startup")
async def cache_model():
    download_model_from_minio(f"", "downloaded_model") # MODEL_PATH : 어제 test 시 "test_download" 사용
    app.state.model, app.state.tokenizer = load_model()

#if __name__ == '__main__':
    #uvicorn.run('main:app', reload=True)

#@app.on_event("startup")
#async def startup_event():
#    start_redis_subscriber()

@app.get("/")
async def root():
    return {"message": "Hello World"}
