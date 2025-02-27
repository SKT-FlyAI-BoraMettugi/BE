
from typing import Any

def get_tokenizer() -> Any:
    return app.state.tokenizer

def get_model() -> Any: 
    return app.state.model

# def get_device():
#     return app.state.device
