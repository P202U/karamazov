from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# The STAR Breakdown we fixed earlier
class STARAnalysis(BaseModel):
    situation_detected: bool
    task_detected: bool
    action_detected: bool
    result_detected: bool
    score: int
    feedback_text: str
    suggested_improvement: str


# What the frontend gets back during a chat
class MessageRead(BaseModel):
    id: int
    role: str
    content: str
    analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
