from google import genai
from app.core.config import settings
from app.core.prompts import SYSTEM_INTERVIEWER_PROMPT
from typing import Sequence
from app.models.message import Message

# Initialize the Client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_next_question(
    jd: str, resume: str, history: Sequence[Message]
) -> str:
    # System Persona
    instruction = SYSTEM_INTERVIEWER_PROMPT.format(
        job_description=jd, resume_text=resume
    )

    # 2. Format Chat History
    chat_history = []
    for msg in history:
        role = "user" if msg.role == "candidate" else "model"
        chat_history.append({"role": role, "parts": [{"text": msg.content}]})

    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash",
        contents=chat_history,
        config={"system_instruction": instruction, "temperature": 0.7},
    )

    if not response or not response.text:
        return "I apologize, but I'm having trouble formulating the next question. Could you please repeat your last point?"

    return response.text
