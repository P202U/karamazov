from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    role: str  # "interviewer" or "candidate"
    content: str
    analysis: Optional[Dict[str, Any]] = None


class MessageCreate(MessageBase):
    interview_id: int


class MessageRead(BaseModel):
    id: int
    role: str
    content: str
    analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
