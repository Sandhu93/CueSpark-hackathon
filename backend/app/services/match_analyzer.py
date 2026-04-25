"""JD-resume match analysis service.

Mock mode returns deterministic placeholder results.
Real mode calls OpenAI chat completions with a structured prompt and parses the
JSON response into a MatchAnalysisResult.
"""
from __future__ import annotations

import json
import re

from loguru import logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.match import MatchAnalysisResult
from app.services import llm
from app.services.prompts import MATCH_ANALYSIS_V1


def _mock_result(jd_text: str, resume_text: str) -> MatchAnalysisResult:
    return MatchAnalysisResult(
        role_title="Mock Role",
        role_key="mock_role",
        seniority_level="mid",
        match_score=72,
        matched_skills=["communication", "problem solving"],
        missing_skills=["domain expertise"],
        risk_areas=["limited evidence of leadership"],
        interview_focus_areas=["past project delivery", "technical depth"],
    )


def _parse_llm_json(raw: str) -> dict:
    """Extract the first JSON object from an LLM text response."""
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {raw[:200]!r}")
    return json.loads(match.group())


def analyze_match(
    jd_text: str,
    resume_text: str,
    *,
    db: Session | None = None,
    session_id: str | None = None,
) -> MatchAnalysisResult:
    """Return a structured match analysis for the given JD and resume.

    If session_id and db are provided, writes match_score, role_title, and
    role_key back to the InterviewSession row (caller must commit).
    """
    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("match_analyzer: mock mode — returning placeholder result")
        result = _mock_result(jd_text, resume_text)
    else:
        prompt = MATCH_ANALYSIS_V1.format(jd_text=jd_text, resume_text=resume_text)
        raw = llm.chat(
            messages=[{"role": "user", "content": prompt}],
            model=settings.openai_chat_model,
        )
        data = _parse_llm_json(raw)
        result = MatchAnalysisResult(**data)
        logger.info(
            "match_analyzer: real LLM result role_key={} match_score={}",
            result.role_key,
            result.match_score,
        )

    if db is not None and session_id is not None:
        _persist_to_session(db, session_id, result)

    return result


def _persist_to_session(db: Session, session_id: str, result: MatchAnalysisResult) -> None:
    from app.models.session import InterviewSession  # local import to avoid circular

    session = db.get(InterviewSession, session_id)
    if session is None:
        logger.warning("match_analyzer: session {} not found; skipping persist", session_id)
        return

    session.match_score = result.match_score
    session.role_title = result.role_title
    session.role_key = result.role_key
    logger.info(
        "match_analyzer: updated session {} — match_score={} role_key={}",
        session_id,
        result.match_score,
        result.role_key,
    )
