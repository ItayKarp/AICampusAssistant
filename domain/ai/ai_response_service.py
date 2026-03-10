import json
import os
from pathlib import Path
from typing import Any, Literal, TypeAlias

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "responder_system_instructions.txt"
RESPONSE_SYSTEM_INSTRUCTIONS = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")


ResponderStatus: TypeAlias = Literal[
    "answered",
    "clarification_needed",
    "not_found",
    "permission_denied",
    "error",
]

ResponderAnswerType: TypeAlias = Literal[
    "direct",
    "summary",
    "list",
    "clarification",
    "fallback",
    "denial",
    "error",
]


class Citation(BaseModel):
    source: str
    fields: list[str]


class ResponseMeta(BaseModel):
    category: str
    table: str
    result_count: int
    scope: str
    intent: str


class ResponderOutput(BaseModel):
    status: ResponderStatus
    answer: str
    answer_type: ResponderAnswerType
    confidence: float = Field(ge=0.0, le=1.0)
    needs_clarification: bool
    clarification_question: str | None
    used_fallback: bool
    fallback_reason: str | None
    citations: list[Citation]
    meta: ResponseMeta


class AIResponseService:
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash-lite",
        ai_client=client,
        system_instruction: str = RESPONSE_SYSTEM_INSTRUCTIONS,
    ):
        self.client = ai_client
        self.model_name = model_name
        self.system_instruction = system_instruction

    def generate_answer(
        self,
        question: str,
        classification,
        repository_result: dict[str, Any],
    ) -> dict[str, Any]:
        if not classification.is_valid:
            return self._build_invalid_classification_response(classification).model_dump()

        if not classification.has_permission:
            return self._build_permission_denied_response(classification).model_dump()

        ai_output = self._generate_with_ai(
            question=question,
            classification=classification,
            repository_result=repository_result,
        )
        return ai_output.model_dump()

    def _generate_with_ai(
        self,
        question: str,
        classification,
        repository_result: dict[str, Any],
    ) -> ResponderOutput:
        payload = self._build_payload(
            question=question,
            classification=classification,
            repository_result=repository_result,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=json.dumps(payload, ensure_ascii=False, indent=2),
            config=GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.2,
                response_mime_type="application/json",
            ),
        )

        raw_text = (response.text or "").strip()

        try:
            parsed = json.loads(raw_text)
            return ResponderOutput.model_validate(parsed)
        except (json.JSONDecodeError, ValidationError):
            return self._build_invalid_ai_output_response(
                classification=classification,
                repository_result=repository_result,
            )

    @staticmethod
    def _build_payload(
        question: str,
        classification,
        repository_result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "question": question,
            "validated_classification": classification.model_dump(),
            "repo_result": repository_result,
        }

    @staticmethod
    def _build_meta(
        classification,
        repository_result: dict[str, Any] | None = None,
    ) -> ResponseMeta:
        result_count = 0
        if repository_result is not None:
            results = repository_result.get("results", [])
            result_count = len(results)

        return ResponseMeta(
            category=getattr(classification, "category", "unknown") or "unknown",
            table=getattr(classification, "table", "unknown") or "unknown",
            result_count=result_count,
            scope=getattr(classification, "scope", "unknown") or "unknown",
            intent=getattr(classification, "intent", "unknown") or "unknown",
        )

    @staticmethod
    def _build_permission_denied_response(classification) -> ResponderOutput:
        classification_confidence = getattr(classification, "confidence", 0.95) or 0.95

        return ResponderOutput(
            status="permission_denied",
            answer="You do not have permission to access that information.",
            answer_type="denial",
            confidence=min(float(classification_confidence), 0.95),
            needs_clarification=False,
            clarification_question=None,
            used_fallback=False,
            fallback_reason=None,
            citations=[],
            meta=AIResponseService._build_meta(classification),
        )

    @staticmethod
    def _build_invalid_classification_response(classification) -> ResponderOutput:
        return ResponderOutput(
            status="error",
            answer="I couldn't complete that request because the classification was invalid.",
            answer_type="error",
            confidence=0.22,
            needs_clarification=False,
            clarification_question=None,
            used_fallback=True,
            fallback_reason="invalid_classification",
            citations=[],
            meta=AIResponseService._build_meta(classification),
        )

    @staticmethod
    def _build_invalid_ai_output_response(
        classification,
        repository_result: dict[str, Any],
    ) -> ResponderOutput:
        repo_success = repository_result.get("success", False)
        repo_results = repository_result.get("results", [])
        repo_message = repository_result.get("message")

        status: ResponderStatus
        answer_type: ResponderAnswerType
        fallback_reason: str
        confidence: float
        answer: str

        if not repo_success:
            answer = repo_message or "I couldn't complete that request because the data response failed."
            status = "error"
            answer_type = "error"
            fallback_reason = "repo_error"
            confidence = 0.25
        elif not repo_results:
            category = getattr(classification, "category", "unknown")
            answer = {
                "faq": "I couldn't find an active FAQ entry matching that request.",
                "exams": "I couldn't find exam data for that request.",
                "courses": "I couldn't find a course matching that request.",
                "office_opening_hours": "I couldn't find opening hours for that office.",
                "announcements": "I couldn't find any matching announcements.",
                "personnel": "I couldn't find personnel information matching that request.",
            }.get(category, "I couldn't find any matching information.")
            status = "not_found"
            answer_type = "fallback"
            fallback_reason = "no_results"
            confidence = 0.40
        else:
            answer = "I couldn't format the final answer reliably, even though matching data was found."
            status = "error"
            answer_type = "error"
            fallback_reason = "invalid_ai_output"
            confidence = 0.30

        return ResponderOutput(
            status=status,
            answer=answer,
            answer_type=answer_type,
            confidence=confidence,
            needs_clarification=False,
            clarification_question=None,
            used_fallback=True,
            fallback_reason=fallback_reason,
            citations=[],
            meta=AIResponseService._build_meta(classification, repository_result),
        )