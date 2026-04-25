"""Candidate-vs-benchmark gap analysis service.

Compares a candidate's resume against a list of retrieved benchmark profiles
and produces a structured BenchmarkAnalysisResult.

Mock mode returns deterministic placeholder data so the full pipeline works
without an OpenAI API key.  Real mode calls the centralized LLM client with
BENCHMARK_ANALYSIS_V1 and parses the JSON response.

The result is persisted as a BenchmarkComparison row and the three score fields
on the InterviewSession row are updated.  Caller is responsible for committing.
"""
from __future__ import annotations

import json
import re
import uuid

from loguru import logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.benchmark_profile import BenchmarkProfile
from app.schemas.benchmark import BenchmarkAnalysisResult
from app.services import llm
from app.services.prompts import BENCHMARK_ANALYSIS_V1


# ── pure helpers ──────────────────────────────────────────────────────────────

def _mock_result() -> BenchmarkAnalysisResult:
    return BenchmarkAnalysisResult(
        benchmark_similarity_score=65,
        resume_competitiveness_score=70,
        evidence_strength_score=60,
        missing_skills=["system design at scale", "mentoring junior engineers"],
        weak_skills=["stakeholder communication", "cross-team delivery"],
        missing_metrics=["quantified impact on revenue or cost", "team size led"],
        weak_ownership_signals=["no evidence of end-to-end project ownership"],
        interview_risk_areas=[
            "limited evidence of leadership under pressure",
            "no metrics backing key project claims",
        ],
        recommended_resume_fixes=[
            "Add measurable outcomes to each role (e.g. % improvement, $savings)",
            "Describe scope of ownership explicitly (team size, budget, SLA)",
        ],
        question_targets=[
            "Walk me through a project where you owned delivery end-to-end.",
            "What metrics did you use to measure success in your last role?",
            "Describe a time you had to influence without authority.",
        ],
    )


def _parse_llm_json(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {raw[:200]!r}")
    return json.loads(match.group())


def _format_benchmark_summaries(profiles: list[BenchmarkProfile]) -> str:
    """Compact text summary of benchmark profiles for the LLM prompt.

    Uses skills, impact_signals, and ownership_signals only — never resume_text.
    """
    lines: list[str] = []
    for i, p in enumerate(profiles, 1):
        lines.append(f"Benchmark {i}: {p.role_title} ({p.seniority_level})")
        if p.skills:
            lines.append(f"  Skills: {', '.join(str(s) for s in p.skills[:12])}")
        if p.impact_signals:
            lines.append(f"  Impact: {'; '.join(str(s) for s in p.impact_signals[:5])}")
        if p.ownership_signals:
            lines.append(f"  Ownership: {'; '.join(str(s) for s in p.ownership_signals[:5])}")
        lines.append("")
    return "\n".join(lines).strip()


# ── persistence helpers ───────────────────────────────────────────────────────

def _persist_comparison(
    db: Session,
    session_id: str,
    role_key: str,
    profiles: list[BenchmarkProfile],
    result: BenchmarkAnalysisResult,
) -> BenchmarkComparison:
    row = BenchmarkComparison(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role_key=role_key,
        benchmark_profile_ids=[p.id for p in profiles],
        benchmark_similarity_score=result.benchmark_similarity_score,
        resume_competitiveness_score=result.resume_competitiveness_score,
        evidence_strength_score=result.evidence_strength_score,
        missing_skills=result.missing_skills,
        weak_skills=result.weak_skills,
        missing_metrics=result.missing_metrics,
        weak_ownership_signals=result.weak_ownership_signals,
        interview_risk_areas=result.interview_risk_areas,
        recommended_resume_fixes=result.recommended_resume_fixes,
        question_targets=result.question_targets,
    )
    db.add(row)
    logger.info(
        "benchmark_analyzer: stored comparison row for session_id={} role_key={}",
        session_id,
        role_key,
    )
    return row


def _update_session_scores(
    db: Session,
    session_id: str,
    result: BenchmarkAnalysisResult,
) -> None:
    from app.models.session import InterviewSession  # local import — avoids circular

    session = db.get(InterviewSession, session_id)
    if session is None:
        logger.warning(
            "benchmark_analyzer: session {} not found — skipping score update",
            session_id,
        )
        return

    session.benchmark_similarity_score = result.benchmark_similarity_score
    session.resume_competitiveness_score = result.resume_competitiveness_score
    session.evidence_strength_score = result.evidence_strength_score
    logger.info(
        "benchmark_analyzer: updated session {} scores — "
        "similarity={} competitiveness={} evidence={}",
        session_id,
        result.benchmark_similarity_score,
        result.resume_competitiveness_score,
        result.evidence_strength_score,
    )


# ── public API ────────────────────────────────────────────────────────────────

def analyze_candidate_vs_benchmark(
    resume_text: str,
    benchmark_profiles: list[BenchmarkProfile],
    *,
    role_key: str,
    session_id: str,
    db: Session,
) -> BenchmarkAnalysisResult:
    """Compare the candidate resume against benchmark profiles.

    Persists a BenchmarkComparison row and updates session score fields.
    Caller must commit the session after this call.

    Returns the structured BenchmarkAnalysisResult regardless of whether
    persistence succeeded.
    """
    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("benchmark_analyzer: mock mode — returning placeholder result")
        result = _mock_result()
    else:
        summaries = _format_benchmark_summaries(benchmark_profiles)
        prompt = BENCHMARK_ANALYSIS_V1.format(
            resume_text=resume_text,
            benchmark_summaries=summaries,
        )
        raw = llm.chat(
            messages=[{"role": "user", "content": prompt}],
            model=settings.openai_chat_model,
        )
        data = _parse_llm_json(raw)
        result = BenchmarkAnalysisResult(**data)
        logger.info(
            "benchmark_analyzer: real LLM result similarity={} competitiveness={}",
            result.benchmark_similarity_score,
            result.resume_competitiveness_score,
        )

    _persist_comparison(db, session_id, role_key, benchmark_profiles, result)
    _update_session_scores(db, session_id, result)
    return result
