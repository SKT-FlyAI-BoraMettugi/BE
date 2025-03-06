import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from dependencies import get_tokenizer, get_model

MODEL_PATH = "downloaded_model"

def load_model():
    base_model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"
    lora_model_path = MODEL_PATH
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True  # 8-bit 양자화
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        device_map="auto",
        quantization_config=quantization_config
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    # LoRA 모델 적용
    model = PeftModel.from_pretrained(base_model, lora_model_path)
    model = model.merge_and_unload()  # LoRA를 병합하여 모델 최적화

    # Tokenizer 설정
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer
