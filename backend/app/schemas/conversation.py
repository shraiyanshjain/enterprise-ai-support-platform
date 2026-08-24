from datetime import datetime

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    user_id: int


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }