from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    role: str  # "interviewer" or "candidate"
    content: str
    analysis: Optional[Dict[str, Any]] = None


class MessageCreate(MessageBase):
    interview_id: int


class MessageRead(MessageBase):
    id: int
    created_at: datetime

    # Pydantic v2 configuration to allow reading from SQLModel/SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
