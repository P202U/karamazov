from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class STARAnalysis(BaseModel):
    situation_detected: bool
    task_detected: bool
    action_detected: bool
    result_detected: bool
    score: int
    feedback_text: str
    suggested_improvement: str


class UploadResponse(BaseModel):
    status: str
    session_id: int
    message: str


class NextQuestionResponse(BaseModel):
    question: str
    analysis: Dict


class InterviewReport(BaseModel):
    average_score: float
    star_completion_rate: Dict[str, str]
    overall_feedback: List[Optional[str]]
    total_exchanges: int


class NextQuestionRequest(BaseModel):
    user_message: str
