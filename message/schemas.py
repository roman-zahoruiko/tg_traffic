from pydantic import BaseModel
from datetime import datetime


class MessageCreateSchema(BaseModel):
    bottoken: str
    chatid: int
    message: str


class MessageResponseSchema(BaseModel):
    id: int
    author_id: int
    response: str
    created_at: datetime

    class Config:
        from_attributes = True
