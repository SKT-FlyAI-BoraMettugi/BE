from fastapi import FastAPI

# FastAPI 인스턴스를 안전하게 가져오는 함수
def get_app():
    from main import app  # ✅ 함수 내부에서 import (순환 참조 방지)
    return app

def get_tokenizer():
    return get_app().state.tokenizer

def get_model():
    return get_app().state.model
