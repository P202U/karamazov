from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from app.utils.datetime import get_utc_now


class InterviewSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jd_text: str
    resume_text: str
    created_at: datetime = Field(default_factory=get_utc_now, nullable=False)
