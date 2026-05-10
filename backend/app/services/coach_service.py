from google import genai
from app.core.config import settings
from app.core.prompts import SYSTEM_INTERVIEWER_PROMPT
from typing import Sequence
from app.models.message import Message

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_next_question(
    jd: str, resume: str, history: Sequence[Message]
) -> str:
    instruction = SYSTEM_INTERVIEWER_PROMPT.format(
        job_description=jd, resume_text=resume
    )
    chat_history = []
    for msg in history:
        role = "user" if msg.role == "candidate" else "model"
        chat_history.append({"role": role, "parts": [{"text": msg.content}]})

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=chat_history,
            config={"system_instruction": instruction, "temperature": 0.7},
        )
        if not response or not response.text:
            return "Could you elaborate on your last point?"
        return response.text
    except Exception as e:
        print(f"Error in coach_service: {e}")
        return "I'm having trouble formulating the next question — could you expand on what you just said?"
