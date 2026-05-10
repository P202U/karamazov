from typing import List, Dict, Any
from app.services import coach_service, judge_service
from app.models.message import Message


class LLMService:
    """
    Orchestrates all LLM interactions.
    Acts as the single point of contact for the 'Coach' and 'Judge'.
    """

    @staticmethod
    async def get_next_interview_question(
        jd: str, resume: str, history: List[Message]
    ) -> str:
        """
        Coordinates the generation of the next interviewer question.
        """
        try:
            question = await coach_service.generate_next_question(
                jd=jd, resume=resume, history=history
            )
            return question
        except Exception as e:
            # Fallback if the LLM service is down or rate-limited
            print(f"Coach Service Error: {e}")
            return "That's interesting. Can you elaborate more on your recent project experience?"

    @staticmethod
    async def analyze_candidate_answer(answer_text: str) -> Dict[str, Any]:
        """
        Coordinates the STAR analysis of the candidate's response.
        """
        try:
            analysis = await judge_service.analyze_answer(answer_text)
            return analysis
        except Exception as e:
            print(f"Judge Service Error: {e}")
            # Return an empty/neutral STAR state so the UI doesn't break
            return {
                "situation_detected": False,
                "task_detected": False,
                "action_detected": False,
                "result_detected": False,
                "score": 0,
                "feedback_text": "Analysis temporarily unavailable.",
                "suggested_improvement": "Continue with your next answer.",
            }


# Instantiate as a singleton for easy import
llm_service = LLMService()
