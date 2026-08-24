from pydantic import BaseModel


class ChatRequest(BaseModel):
    content: str


class ChatResponse(BaseModel):
    user_message: str
    assistant_message: str