from __future__ import annotations

import json
import re

from loguru import logger

from app.core.config import settings
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion
from app.schemas.agent_results import BenchmarkGapCoverageResult
from app.services import llm
from app.services.prompts import BENCHMARK_GAP_COVERAGE_V1


def analyze_benchmark_gap_coverage(
    *,
    question: InterviewQuestion,
    answer: CandidateAnswer,
    modality_summaries: list[dict] | None = None,
) -> BenchmarkGapCoverageResult:
    candidate_response = _candidate_response_text(answer)
    gap_refs = [str(gap) for gap in (question.benchmark_gap_refs or []) if str(gap).strip()]

    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("benchmark_gap_agent: mock mode for answer_id={}", answer.id)
        return _mock_result(gap_refs=gap_refs, candidate_response=candidate_response)

    prompt = BENCHMARK_GAP_COVERAGE_V1.format(
        question_text=question.question_text,
        expected_signal=question.expected_signal or "No expected signal provided.",
        benchmark_gap_refs="\n".join(f"- {gap}" for gap in gap_refs) or "No benchmark gap refs.",
        candidate_response=candidate_response or "No candidate response text available.",
        modality_summaries=json.dumps(modality_summaries or [], ensure_ascii=False),
    )
    raw = llm.chat(
        messages=[{"role": "user", "content": prompt}],
        model=settings.openai_chat_model,
    )
    data = _parse_json_object(raw)
    return BenchmarkGapCoverageResult(**data)


def _candidate_response_text(answer: CandidateAnswer) -> str:
    parts = [
        answer.transcript,
        answer.text_answer,
        answer.code_answer,
    ]
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def _mock_result(
    *,
    gap_refs: list[str],
    candidate_response: str,
) -> BenchmarkGapCoverageResult:
    if not gap_refs:
        gap_refs = ["core role benchmark gap"]

    lower_response = candidate_response.lower()
    covered = [
        gap
        for gap in gap_refs
        if any(token in lower_response for token in _gap_tokens(gap))
    ]
    if not covered and candidate_response.strip():
        covered = gap_refs[:1]
    missed = [gap for gap in gap_refs if gap not in covered]
    score = 7 if covered else 3
    if missed:
        score = min(score, 6)
    evidence_quality = "strong" if score >= 8 else "moderate" if score >= 5 else "weak"

    return BenchmarkGapCoverageResult(
        benchmark_gap_coverage_score=score,
        covered_gaps=covered,
        missed_gaps=missed,
        evidence_quality=evidence_quality,
        gap_specific_feedback=(
            "The response gives some benchmark-relevant evidence, but should connect the "
            "example more directly to measurable impact and ownership."
            if covered
            else "The response does not provide direct evidence for the benchmark gap."
        ),
        remaining_interview_risk=(
            "Follow up on the missed benchmark gap(s): " + "; ".join(missed)
            if missed
            else "Risk is reduced for the referenced benchmark gap, but follow-up may still probe depth."
        ),
    )


def _gap_tokens(gap: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", gap.lower())
        if len(token) >= 4
    ]


def _parse_json_object(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in benchmark gap response: {raw[:200]!r}")
    return json.loads(match.group())
