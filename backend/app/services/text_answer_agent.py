from __future__ import annotations

import json
import re

from loguru import logger

from app.core.config import settings
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion
from app.schemas.agent_results import TextAnswerAnalysisResult
from app.services import llm
from app.services.prompts import TEXT_ANSWER_ANALYSIS_V1


def analyze_text_answer(
    *,
    question: InterviewQuestion,
    answer: CandidateAnswer,
) -> TextAnswerAnalysisResult:
    written_answer = _written_answer_text(answer)
    if not written_answer:
        raise ValueError("Candidate answer has no written text to analyze")

    gap_refs = [str(gap) for gap in (question.benchmark_gap_refs or []) if str(gap).strip()]

    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("text_answer_agent: mock mode for answer_id={}", answer.id)
        return _mock_result(
            written_answer=written_answer,
            expected_signal=question.expected_signal or "",
            gap_refs=gap_refs,
        )

    prompt = TEXT_ANSWER_ANALYSIS_V1.format(
        question_text=question.question_text,
        expected_signal=question.expected_signal or "No expected signal provided.",
        benchmark_gap_refs="\n".join(f"- {gap}" for gap in gap_refs) or "No benchmark gap refs.",
        written_answer=written_answer,
    )
    raw = llm.chat(
        messages=[{"role": "user", "content": prompt}],
        model=settings.openai_chat_model,
    )
    data = _parse_json_object(raw)
    return TextAnswerAnalysisResult(**data)


def _written_answer_text(answer: CandidateAnswer) -> str:
    parts = [answer.text_answer]
    if answer.code_answer:
        parts.append(f"Code or pseudocode:\n{answer.code_answer}")
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def _mock_result(
    *,
    written_answer: str,
    expected_signal: str,
    gap_refs: list[str],
) -> TextAnswerAnalysisResult:
    word_count = len(re.findall(r"[A-Za-z0-9']+", written_answer))
    has_structure = _has_any(written_answer, ["first", "then", "because", "therefore", "finally"])
    has_specificity = _has_any(written_answer, ["%", "latency", "users", "requests", "revenue", "cost"])
    has_evidence = _has_any(written_answer, ["owned", "measured", "reduced", "improved", "increased"])
    gap_hits = sum(1 for gap in gap_refs if _gap_is_referenced(written_answer, gap))

    relevance = 8 if _overlap_score(written_answer, expected_signal) > 0 else 6
    structure = 8 if has_structure else 5
    specificity = 8 if has_specificity else 5
    evidence = 8 if has_evidence else 5
    clarity = 8 if word_count >= 25 else 6
    completeness = 8 if word_count >= 60 else 6 if word_count >= 25 else 4

    if gap_refs and gap_hits == 0:
        relevance = min(relevance, 6)
        evidence = min(evidence, 5)

    strengths = []
    weaknesses = []
    suggestions = []
    if has_evidence:
        strengths.append("Includes concrete action or impact evidence.")
    else:
        weaknesses.append("Written answer lacks concrete evidence.")
        suggestions.append("Add a specific example with measurable outcome.")
    if has_structure:
        strengths.append("Uses a readable structure.")
    else:
        weaknesses.append("Answer structure is not explicit enough.")
        suggestions.append("Use context, action, result, and follow-up structure.")
    if gap_refs and gap_hits:
        strengths.append("References at least one benchmark gap target.")
    elif gap_refs:
        weaknesses.append("Does not directly address the benchmark gap references.")
        suggestions.append("Tie the written answer directly to the benchmark gap being tested.")

    return TextAnswerAnalysisResult(
        relevance_score=relevance,
        structure_score=structure,
        specificity_score=specificity,
        evidence_score=evidence,
        clarity_score=clarity,
        completeness_score=completeness,
        strengths=strengths or ["Written answer is understandable."],
        weaknesses=weaknesses,
        improvement_suggestions=suggestions,
    )


def _has_any(text: str, needles: list[str]) -> bool:
    lower = text.lower()
    return any(needle in lower for needle in needles)


def _overlap_score(answer_text: str, expected_signal: str) -> int:
    expected_tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", expected_signal.lower())
        if len(token) >= 4
    }
    answer_tokens = set(re.findall(r"[a-z0-9]+", answer_text.lower()))
    return len(expected_tokens & answer_tokens)


def _gap_is_referenced(answer_text: str, gap: str) -> bool:
    answer_tokens = set(re.findall(r"[a-z0-9]+", answer_text.lower()))
    gap_tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", gap.lower())
        if len(token) >= 4
    }
    return bool(answer_tokens & gap_tokens)


def _parse_json_object(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in text answer response: {raw[:200]!r}")
    return json.loads(match.group())
