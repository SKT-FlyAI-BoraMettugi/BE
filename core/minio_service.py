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

# minio에서 모델 다운로드
def download_model_from_minio(model_s3_path: str, local_dir: str):
    """
    MinIO에서 모델 전체 다운로드
    :param model_s3_path: MinIO 내 저장된 모델 경로 (예: "llama_model/")
    :param local_dir: 로컬에 저장할 경로 (예: "./downloaded_model/")
    """
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


# def download_test_from_minio(model_path: str, local_save_path: str):
#     """
#     MinIO에서 파일 다운로드 (예: test.txt)
#     :param model_path: MinIO 내 저장된 파일 경로 (예: test_folder/test.txt)
#     :param local_save_path: 로컬에 저장할 경로 (예: ./downloaded_model/test.txt)
#     """
#     try:
#         os.makedirs(os.path.dirname(local_save_path), exist_ok=True)  # 로컬 저장 폴더 생성
#         s3.download_file("test", model_path, local_save_path)
#         print(f"✅ {model_path} 다운로드 완료 → {local_save_path}")
#         return local_save_path
#     except Exception as e:
#         print(f"❌ MinIO에서 {model_path} 다운로드 실패: {e}")
#         return None