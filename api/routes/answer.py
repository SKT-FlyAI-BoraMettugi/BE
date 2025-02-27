from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.answer import get_answer_history, get_answer_scores
from schemas.answer import AnswerResponse, AnswerScoreResponse, AnswerSubmit
from crud.model_inference import get_tokenizer, get_model # , get_device

router = APIRouter()

@router.get("/history/{user_id}/{question_id}", response_model=list[AnswerResponse])
async def get_answer_history_api(user_id: int, question_id: int, db: Session = Depends(get_db)):
    answers = get_answer_history(db, user_id, question_id)
    
    if not answers:
        raise HTTPException(status_code=404, detail="답변 이력이 없습니다.")

    return answers

@router.get("/{user_id}/{question_id}", response_model=AnswerScoreResponse)
async def get_answer_scores_api(user_id: int, question_id: int, db: Session = Depends(get_db)):
    answer_scores = get_answer_scores(db, user_id, question_id)
    
    if not answer_scores:
        raise HTTPException(status_code=404, detail="채점 결과를 찾을 수 없습니다.")

    return answer_scores

# 문제 답안 제출 == 채점
@router.post("/{user_id}/{question_id}")
async def grade_answers(
    user_id: int, question_id: int, 
    answer_data: AnswerSubmit, tokenizer = Depends(get_tokenizer), model = Depends(get_model), 
    db: Session = Depends(get_db) # device: str = Depends(get_device), 
):
    
    # 1. 사용자 답변 불러오기
    input_text = answer_data.answer
    # 2. 모델에 넣을 수 있도록 토큰화 ########################## pt 맞는지 확인 ###
    inputs = tokenizer(input_text, return_tensors="pt") 

    # 3. 모델 추론 수행
    with torch.no_grad():
        outputs = model(**inputs)

    # 4. 모델 결과 가공 ########################## 실제 결과에 맞게 수정 필요 ###
    scores = outputs["scores"].tolist()  # [창의, 논리, 사고, 설득, 깊이]
    reviews = outputs["explanations"]  # ["창의성 설명", "논리 설명", ...]

    total_score = sum(scores) / len(scores) if scores else 0

    # 5. DB에 저장 : 기존 답변 O (값 update), X (db에 새로 add)
    existing_answer = db.query(Answer).filter(
        Answer.user_id == user_id, 
        Answer.question_id == question_id
    ).first()

    if existing_answer:
        # 기존 데이터가 있으면 업데이트
        existing_answer.content = input_text
        existing_answer.creativity = scores[0]
        existing_answer.logic = scores[1]
        existing_answer.thinking = scores[2]
        existing_answer.persuasion = scores[3]
        existing_answer.depth = scores[4]
        existing_answer.creativity_review = reviews[0]
        existing_answer.logic_review = reviews[1]
        existing_answer.thinking_review = reviews[2]
        existing_answer.persuasion_review = reviews[3]
        existing_answer.depth_review = reviews[4]
        existing_answer.total_score = total_score
    else:
        # 기존 데이터가 없으면 새로 추가
        new_answer = Answer(
            user_id=user_id,
            question_id=question_id,
            content=input_text,
            creativity=scores[0],
            logic=scores[1],
            thinking=scores[2],
            persuasion=scores[3],
            depth=scores[4],
            creativity_review=reviews[0],
            logic_review=reviews[1],
            thinking_review=reviews[2],
            persuasion_review=reviews[3],
            depth_review=reviews[4],
            total_score=total_score
        )
        db.add(new_answer)

    # DB 반영
    db.commit()

    return  # 응답 없이 종료 / FastAPI는 자동으로 200 OK 반환