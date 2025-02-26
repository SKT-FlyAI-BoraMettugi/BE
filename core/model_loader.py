import os
import torch
from config import minio_client, bucket_name

MODEL_PATH = "models/llama_model.safetensors"

# 모델 다운로드 함수
def download_model():
    """MinIO에서 모델을 다운로드하여 로컬에 저장"""
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from MinIO...")
        minio_client.fget_object(bucket_name, "llama/finetuned_model.safetensors", MODEL_PATH)
        print("Model downloaded.")

# 모델 로드 함수
def load_model():
    """모델을 로드하고 FastAPI에서 사용 가능하게 설정"""
    download_model()  # MinIO에서 모델 다운로드
    print("Loading Llama model...")
    model = torch.load(MODEL_PATH, map_location="cpu")  # CPU 또는 GPU로 로드
    model.eval()  # 모델을 평가 모드로 설정
    print("Model loaded successfully!")
    return model

# 모델 로드
llama_model = load_model()
