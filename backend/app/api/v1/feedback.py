from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api import deps
from app.models.message import Message

router = APIRouter()


@router.get("/{session_id}")
async def get_interview_report(session_id: int, db: Session = Depends(deps.get_db)):
    # 1. Fetch all candidate messages that have an analysis
    statement = select(Message).where(
        Message.interview_id == session_id, Message.role == "candidate"
    )
    messages = db.exec(statement).all()

    if not messages:
        raise HTTPException(
            status_code=404, detail="No interview data found for this session."
        )

    # 2. Aggregate Stats
    total_score = 0
    star_counts = {"S": 0, "T": 0, "A": 0, "R": 0}
    feedback_points = []

    for msg in messages:
        analysis = msg.analysis
        if analysis:
            total_score += analysis.get("score", 0)
            if analysis.get("situation_detected"):
                star_counts["S"] += 1
            if analysis.get("task_detected"):
                star_counts["T"] += 1
            if analysis.get("action_detected"):
                star_counts["A"] += 1
            if analysis.get("result_detected"):
                star_counts["R"] += 1
            feedback_points.append(analysis.get("feedback_text"))

    # 3. Compile Final Summary
    num_answers = len(messages)
    return {
        "average_score": round(total_score / num_answers, 1) if num_answers > 0 else 0,
        "star_completion_rate": {
            k: f"{round((v / num_answers) * 100)}%" for k, v in star_counts.items()
        },
        "overall_feedback": feedback_points,
        "total_exchanges": num_answers,
    }
