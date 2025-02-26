from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.question import save_question, get_question_detail
from schemas.question import QuestionCreate, QuestionResponse
from models.question import Question  
from core.minio_service import download_model_from_minio

router = APIRouter()

@router.post("/{user_id}")
async def submit_question(user_id: int, question_data: QuestionCreate, db: Session = Depends(get_db)):
    question = save_question(db, user_id, question_data)
    
    return {"message": "문제 출제 완료", "question_id": question.question_id}
    
# 문제 상세 조회
@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    question = get_question_detail(db, question_id)
    
    if not question:
        raise HTTPException(status_code=404, detail="해당 문제를 찾을 수 없습니다.")
    
    return question

# 문제 답안 제출 == 채점
@router.post("/{user_id}/{question_id}")
async def download_model():

    # 모델 파라미터 가져오기
    """
    MinIO에서 모델 다운로드 API
    4 가지 파일 불러오기
    1.safetensors_files 
    2.adapter_config_files
    3.tokenizer_files
    4.config_files
    """
    model_s3_path = "test_folder/test.txt"  # MinIO에 저장된 경로
    local_path = "./downloaded_model/test.txt" # local 저장 경로

    result = download_model_from_minio(model_s3_path, local_path)

    if result:
        return {"message": "✅ 모델 다운로드 성공!", "local_path": result}
    else:
        return {"error": "❌ 모델 다운로드 실패"}
    
    # 모델 추론 실행


    # 형식에 맞게 output 생성



