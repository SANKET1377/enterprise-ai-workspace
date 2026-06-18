from pydantic import BaseModel
from datetime import datetime


class ChatHistoryResponse(BaseModel):
    id: int
    message: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True