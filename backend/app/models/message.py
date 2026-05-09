from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional, Dict


def get_utc_now():
    return datetime.now(timezone.utc)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    interview_id: int = Field(foreign_key="interviewsession.id")
    role: str
    content: str
    analysis: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=get_utc_now, nullable=False)
