from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.nolly import get_db
from crud.answer import get_answer_history, get_answer_scores
from schemas.answer import AnswerResponse, AnswerScoreResponse, AnswerSubmit
from dependencies import get_tokenizer, get_model
from models.question import Question 
from models.answer import Answer
import torch
import json
import re

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

@router.post("grade/{user_id}/{question_id}")
async def grade_answers(
    user_id: int, question_id: int, 
    answer_data: AnswerSubmit, tokenizer = Depends(get_tokenizer), model = Depends(get_model), 
    db: Session = Depends(get_db) 
):
    question = db.query(Question).filter(
        Question.question_id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="해당 문제를 찾을 수 없습니다.")

    description = question.description  # 문제 설명

    # ✅ 패딩 토큰 명확하게 설정 (경고 방지)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 1. 사용자 답변 불러오기 (JSON 출력을 강제하는 프롬프트 추가)
    input_text = [
        {"role": "system", "content": """답변을 다음 항목으로 나누어 JSON 형식으로 평가해 주세요.
        반드시 JSON 객체 하나로 반환하세요.
        예시:
        {
            "논리력": {"점수": 8, "해설": "설명이 논리적입니다."},
            "사고력": {"점수": 7, "해설": "분석력이 뛰어납니다."},
            "창의력": {"점수": 9, "해설": "새로운 아이디어가 포함되었습니다."},
            "설득력": {"점수": 6, "해설": "설명이 명확합니다."},
            "추론의 깊이": {"점수": 7, "해설": "근거가 논리적입니다."}
        }
        """.strip()},
        {"role": "assistant", "content": f"{description}"},
        {"role": "user", "content": f"{answer_data.answer}"}
    ]

    # 2. 모델에 넣을 수 있도록 토큰화
    inputs = tokenizer.apply_chat_template(
        input_text,
        add_generation_prompt=True,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(model.device)

    terminators = [
        tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    # 3. 모델 추론 수행
    outputs = model.generate(
        inputs,
        max_new_tokens=1024,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.6,
        top_p=0.9
    )

    # 4. 모델 결과 디코딩
    generated_text = tokenizer.decode(outputs[:, inputs.shape[1]:][0], skip_special_tokens=True)
    print("🔍 모델 생성 결과:", generated_text)

    # ✅ JSON 자동 보정 (불완전한 JSON을 수정)
    try:
        # 1️⃣ JSON 내부 개별 `{}` 블록을 하나의 JSON 객체로 병합
        json_str = re.sub(r"}\s*{", "},{", generated_text.strip())  # 중괄호 사이 개행 문제 수정
        json_str = f"{{{json_str.strip()}}}" if not json_str.startswith("{") else json_str  # 중괄호 감싸기
        json_str = json_str.replace("\n", "").replace("\t", "")  # 불필요한 줄바꿈 제거
        json_str = re.sub(r",\s*}", "}", json_str)  # 마지막 쉼표 제거

        result = json.loads(json_str)  # JSON 변환

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"모델 응답을 JSON으로 변환하는데 실패했습니다. 출력된 텍스트: {generated_text}")

    # 5. 점수와 리뷰 추출
    scores = [
        result.get("논리력", {}).get("점수", 0),
        result.get("사고력", {}).get("점수", 0),
        result.get("창의력", {}).get("점수", 0),
        result.get("설득력", {}).get("점수", 0),
        result.get("추론의 깊이", {}).get("점수", 0)
    ]

    reviews = [
        result.get("논리력", {}).get("해설", ""),
        result.get("사고력", {}).get("해설", ""),
        result.get("창의력", {}).get("해설", ""),
        result.get("설득력", {}).get("해설", ""),
        result.get("추론의 깊이", {}).get("해설", "")
    ]

    total_score = sum(scores) / len(scores) if scores else 0

    # 6. DB 저장
    existing_answer = db.query(Answer).filter(
        Answer.user_id == user_id, 
        Answer.question_id == question_id
    ).first()

    if existing_answer:
        existing_answer.content = answer_data.answer
        existing_answer.creativity = scores[2]
        existing_answer.logic = scores[0]
        existing_answer.thinking = scores[1]
        existing_answer.persuasion = scores[3]
        existing_answer.depth = scores[4]
        existing_answer.creativity_review = reviews[2]
        existing_answer.logic_review = reviews[0]
        existing_answer.thinking_review = reviews[1]
        existing_answer.persuasion_review = reviews[3]
        existing_answer.depth_review = reviews[4]
        existing_answer.total_score = total_score
    else:
        db.add(Answer(
            user_id=user_id, question_id=question_id, content=answer_data.answer,
            creativity=scores[2], logic=scores[0], thinking=scores[1],
            persuasion=scores[3], depth=scores[4],
            creativity_review=reviews[2], logic_review=reviews[0],
            thinking_review=reviews[1], persuasion_review=reviews[3], depth_review=reviews[4],
            total_score=total_score
        ))

    db.commit()
    return