from pydantic import BaseModel


class ChatRequest(BaseModel):
    
    msg: str
