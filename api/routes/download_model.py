from fastapi import APIRouter
# from models.model_loader import llama_model
from core.minio_service import download_model_from_minio
import os

router = APIRouter()

@router.get("/")
async def download_model():
    """
    MinIO에서 모델 다운로드 API
    """
    model_s3_path = "test_folder/test.txt"  # MinIO에 저장된 경로
    local_path = "./downloaded_model/test.txt" # local 저장 경로

    result = download_model_from_minio(model_s3_path, local_path)

    if result:
        return {"message": "✅ 모델 다운로드 성공!", "local_path": result}
    else:
        return {"error": "❌ 모델 다운로드 실패"}

