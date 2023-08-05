from pydantic import BaseModel

class BasicReq (BaseModel):
    message: str
    key: str

class LlamaReq (BaseModel):
    message: str
    key: str
    max: int = 32
    temp: float = 0.5