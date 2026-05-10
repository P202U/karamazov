import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, col
from app.api import deps
from app.models.interview import InterviewSession
from app.models.message import Message
from app.services import coach_service, judge_service
from app.schemas.interview import NextQuestionResponse, NextQuestionRequest

router = APIRouter()


@router.post("/{session_id}/next", response_model=NextQuestionResponse)
async def get_next_question(
    session_id: int, body: NextQuestionRequest, db: Session = Depends(deps.get_db)
):
    session_record = db.get(InterviewSession, session_id)
    if not session_record:
        raise HTTPException(status_code=404, detail="Interview session not found")

    user_entry = Message(
        interview_id=session_id, role="candidate", content=body.user_message
    )
    db.add(user_entry)
    db.flush()

    statement = (
        select(Message)
        .where(Message.interview_id == session_id)
        .order_by(col(Message.created_at))
    )
    history = db.exec(statement).all()

    next_question, analysis = await asyncio.gather(
        coach_service.generate_next_question(
            jd=session_record.jd_text,
            resume=session_record.resume_text,
            history=history,
        ),
        judge_service.analyze_answer(body.user_message),
    )

    ai_entry = Message(
        interview_id=session_id, role="interviewer", content=next_question
    )
    db.add(ai_entry)
    user_entry.analysis = analysis

    db.commit()
    db.refresh(ai_entry)

    return {"question": ai_entry.content, "analysis": analysis}
