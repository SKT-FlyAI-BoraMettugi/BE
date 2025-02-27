import os
import torch
from transformers import AutoModel, AutoTokenizer, AutoConfig
from safetensors.torch import load_file
from peft import PeftModel, PeftConfig

MODEL_PATH = "downloaded_model"

def load_tokenizer():
    # Tokenizer 로드
    tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_PATH}/tokenizer.json", local_files_only=True, use_fast=True)
    
    return tokenizer

def load_model():
    # Config 로드
    config = AutoConfig.from_pretrained(f"{MODEL_PATH}/config.json", local_files_only=True) 

    # 모델 생성 (AutoModelForCausalLM, AutoModelForSequenceClassification 등 선택)
    model = AutoModel.from_config(config)

    # .safetensors 로드
    weights = load_file(f"{MODEL_PATH}/model.safetensors") # 파일명 확인

    # 모델에 가중치 적용
    model.load_state_dict(weights, strict=False)

    # # 모델을 GPU로 이동 (선택)
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model.to(device)
    model.eval() # 모델 평가 모드로 설정

    # Adapter 설정 로드
    adapter_config = PeftConfig.from_pretrained(f"{MODEL_PATH}/adapter_config.json", local_files_only=True)

    # Adapter 적용
    model = PeftModel(model, adapter_config)

    return model

# # 모델 로드
# llama_model = load_model()
