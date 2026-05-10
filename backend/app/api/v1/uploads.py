from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlmodel import Session
from app.api import deps
from app.utils.pdf_parser import parse_pdf
from app.models.interview import InterviewSession
from app.schemas.interview import UploadResponse

router = APIRouter()


@router.post("/resume", response_model=UploadResponse)
async def upload_resume(
    jd_text: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
):
    resume_content = await file.read()
    try:
        text = parse_pdf(resume_content)

        # Session record
        new_session = InterviewSession(jd_text=jd_text, resume_text=text)

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return {
            "status": "success",
            "session_id": new_session.id,
            "message": "Resume and JD ingested successfully",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
