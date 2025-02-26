import boto3
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv(override=True)

MINIO_URL = os.getenv("MINIO_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# MinIO 클라이언트 생성
s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_URL}",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def download_model_from_minio(model_path: str, local_save_path: str):
    """
    MinIO에서 파일 다운로드 (예: test.txt)
    :param model_path: MinIO 내 저장된 파일 경로 (예: test_folder/test.txt)
    :param local_save_path: 로컬에 저장할 경로 (예: ./downloaded_model/test.txt)
    """
    try:
        os.makedirs(os.path.dirname(local_save_path), exist_ok=True)  # 로컬 저장 폴더 생성
        s3.download_file(S3_BUCKET_NAME, model_path, local_save_path)
        print(f"✅ {model_path} 다운로드 완료 → {local_save_path}")
        return local_save_path
    except Exception as e:
        print(f"❌ MinIO에서 {model_path} 다운로드 실패: {e}")
        return None
