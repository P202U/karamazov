from typing import Any, Dict
from pydantic import BaseModel
from google import genai
from app.core.config import settings
from app.core.prompts import SYSTEM_JUDGE_PROMPT
from app.schemas.interview import STARAnalysis

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def analyze_answer(answer_text: str) -> Dict[str, Any]:
    """
    Analyzes a candidate's response against the STAR method.
    Uses Gemini 2.0 Flash with a forced JSON schema response.
    """

    user_prompt = f"Evaluate the following interview answer:\n\n{answer_text}"

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config={
                "system_instruction": SYSTEM_JUDGE_PROMPT,
                "temperature": 0.1,
                "response_mime_type": "application/json",
                "response_schema": STARAnalysis,
            },
        )

        # 1. Check if we actually got a response
        if not response or response.parsed is None:
            return _get_fallback_analysis("Analysis unavailable due to model timeout.")

        # 2. Type Guard: Handle Pydantic model return
        if isinstance(response.parsed, BaseModel):
            return response.parsed.model_dump()

        # 3. Type Guard: Handle Dictionary return
        if isinstance(response.parsed, dict):
            return response.parsed

        return _get_fallback_analysis("Unexpected data format returned from AI.")

    except Exception as e:
        print(f"Error in judge_service: {e}")
        return _get_fallback_analysis("Analysis temporarily unavailable.")


def _get_fallback_analysis(error_message: str) -> Dict[str, Any]:
    """Helper to return a valid schema if the AI fails."""
    return {
        "situation_detected": False,
        "task_detected": False,
        "action_detected": False,
        "result_detected": False,
        "score": 1,
        "feedback_text": error_message,
        "suggested_improvement": "Try re-submitting your answer or checking your connection.",
    }
