from pydantic import BaseModel, Field
from typing import Optional, List


# 1. The STAR Breakdown (The specific feedback)
class STARAnalysis(BaseModel):
    situation_detected = bool
    task_detected = bool
    action_detected: bool
    result_detected: bool
    score: int = Field(..., ge=1, le=10)
    feedback_text: str
    suggested_improvement: str


# 2. The Message
class MessageBase(BaseModel):
    role: str  # "interviewer" or "candidate"
    content: str
    analysis: Optional[STARAnalysis] = None


# 3. The Session Start
class InterviewSetup(BaseModel):
    job_description: str
    resume_text: str
    difficulty: str = "Standard"  # e.g., "Standard", "Stress Test"
