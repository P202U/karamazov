from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, col
from app.api import deps
from app.models.interview import InterviewSession
from app.models.message import Message
from app.services import coach_service, judge_service
from app.schemas.interview import NextQuestionResponse

router = APIRouter()


@router.post("/{session_id}/next", response_model=NextQuestionResponse)
async def get_next_question(
    session_id: int, user_message: str, db: Session = Depends(deps.get_db)
):
    # 1. Fetch Session Context
    session_record = db.get(InterviewSession, session_id)
    if not session_record:
        raise HTTPException(status_code=404, detail="Interview session not found")

    # 2. Save User's Message to DB
    user_entry = Message(
        interview_id=session_id, role="candidate", content=user_message
    )
    db.add(user_entry)
    db.commit()

    # 3. Fetch History for the LLM
    statement = (
        select(Message)
        .where(Message.interview_id == session_id)
        .order_by(col(Message.created_at))
    )
    history = db.exec(statement).all()

    # 4. Get Next Question from Gemini (The Coach)
    next_question = await coach_service.generate_next_question(
        jd=session_record.jd_text, resume=session_record.resume_text, history=history
    )

    # 5. Save AI's Question to DB
    ai_entry = Message(
        interview_id=session_id, role="interviewer", content=next_question
    )
    db.add(ai_entry)

    # 6. Trigger STAR Analysis (The Judge)
    analysis = await judge_service.analyze_answer(user_message)
    user_entry.analysis = analysis

    db.commit()
    db.refresh(ai_entry)

    return {
        "question": ai_entry.content,
        "analysis": analysis,
    }
