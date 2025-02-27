import boto3
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv(override=True)

MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_USER = os.getenv("MINIO_USER")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# MinIO 클라이언트 생성
s3 = boto3.client(
    "s3",
    endpoint_url=f"{MINIO_HOST}",
    aws_access_key_id=MINIO_USER,
    aws_secret_access_key=MINIO_PASSWORD
)

# minio에서 모델 다운로드
def download_model_from_minio(model_s3_path: str, local_dir: str):
    try:
        os.makedirs(local_dir, exist_ok=True)  # 로컬 저장 폴더 생성
        
        # MinIO에서 해당 모델 폴더의 모든 객체 가져오기
        objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=model_s3_path)

        if 'Contents' not in objects:
            print(f"❌ MinIO에 {model_s3_path} 경로 없음")
            return None
        
        for obj in objects['Contents']:
            file_key = obj['Key']
            file_name = os.path.basename(file_key)
            local_path = os.path.join(local_dir, file_name)

            s3.download_file(S3_BUCKET_NAME, file_key, local_path)
            print(f"✅ {file_key} 다운로드 완료 → {local_path}")
        
        return local_dir
    except Exception as e:
        print(f"❌ MinIO에서 {model_s3_path} 다운로드 실패: {e}")
        return None
