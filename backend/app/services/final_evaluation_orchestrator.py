from __future__ import annotations

import json
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import AnswerProcessingStatus, CandidateAnswer
from app.models.evaluation import AnswerEvaluation
from app.models.question import ResponseMode
from app.schemas.evaluation import FinalEvaluationResult


def evaluate_answer(db: Session, answer_id: str) -> tuple[FinalEvaluationResult, AnswerEvaluation]:
    answer = db.get(CandidateAnswer, answer_id)
    if answer is None:
        raise ValueError(f"Candidate answer not found: {answer_id}")

    agent_results = list(
        db.execute(
            select(AgentResult).where(
                AgentResult.answer_id == answer_id,
                AgentResult.status == AgentResultStatus.SUCCEEDED.value,
            )
        )
        .scalars()
        .all()
    )
    result = orchestrate_final_evaluation(answer=answer, agent_results=agent_results)
    row = _store_answer_evaluation(db, answer_id=answer_id, result=result)
    answer.processing_status = AnswerProcessingStatus.EVALUATED.value
    return result, row


def orchestrate_final_evaluation(
    *,
    answer: CandidateAnswer,
    agent_results: Iterable[AgentResult],
) -> FinalEvaluationResult:
    mode = ResponseMode(answer.answer_mode or ResponseMode.SPOKEN_ANSWER.value)
    by_type = {result.agent_type: result for result in agent_results}
    benchmark_score = _benchmark_gap_score(by_type.get(AgentType.BENCHMARK_GAP.value))
    communication_score = _communication_score(answer, by_type.get(AgentType.AUDIO.value))
    response_strength = _response_strength(answer)
    code_score = _agent_score(by_type.get(AgentType.CODE_EVALUATION.value), default=response_strength)
    text_score = _agent_score(by_type.get(AgentType.TEXT_ANSWER.value), default=response_strength)

    category_scores = _category_scores_for_mode(
        mode=mode,
        benchmark_score=benchmark_score,
        communication_score=communication_score,
        response_strength=response_strength,
        text_score=text_score,
        code_score=code_score,
    )
    weights = _weights_for_mode(mode, answer)
    overall = round(sum(category_scores[name] * weight for name, weight in weights.items()))
    strengths, weaknesses, improvements = _feedback_lists(
        category_scores,
        benchmark_score=benchmark_score,
        communication_score=communication_score,
    )

    return FinalEvaluationResult(
        overall_score=max(0, min(100, overall)),
        category_scores=category_scores,
        strict_feedback=_strict_feedback(overall, mode, benchmark_score),
        strengths=strengths,
        weaknesses=weaknesses,
        improvement_suggestions=improvements,
        benchmark_gap_summary=_benchmark_summary(by_type.get(AgentType.BENCHMARK_GAP.value)),
        communication_summary=_communication_summary(answer, by_type.get(AgentType.AUDIO.value)),
        modality_breakdown={
            "answer_mode": mode.value,
            "available_agent_results": sorted(by_type.keys()),
            "weights": weights,
        },
    )


def _weights_for_mode(mode: ResponseMode, answer: CandidateAnswer) -> dict[str, float]:
    if mode == ResponseMode.SPOKEN_ANSWER:
        return {
            "benchmark_gap_coverage": 0.30,
            "answer_relevance": 0.20,
            "evidence_examples": 0.20,
            "communication_clarity": 0.15,
            "role_specific_depth": 0.10,
            "audio_professionalism": 0.05,
        }
    if mode == ResponseMode.WRITTEN_ANSWER:
        return {
            "relevance": 0.25,
            "structure": 0.20,
            "evidence_specificity": 0.20,
            "completeness": 0.15,
            "benchmark_gap_coverage": 0.15,
            "clarity": 0.05,
        }
    if mode == ResponseMode.CODE_ANSWER:
        return {
            "code_correctness": 0.35,
            "reasoning_explanation": 0.20,
            "complexity": 0.15,
            "edge_cases": 0.15,
            "readability_testability": 0.10,
            "benchmark_relevance": 0.05,
        }

    weights: dict[str, float] = {"benchmark_gap_coverage": 0.25}
    modalities = []
    if answer.transcript or answer.audio_object_key:
        modalities.append("spoken")
    if answer.text_answer:
        modalities.append("written")
    if answer.code_answer:
        modalities.append("code")
    if not modalities:
        modalities = ["written"]

    share = 0.75 / len(modalities)
    for modality in modalities:
        weights[f"{modality}_quality"] = share
    return weights


def _category_scores_for_mode(
    *,
    mode: ResponseMode,
    benchmark_score: int,
    communication_score: int,
    response_strength: int,
    text_score: int,
    code_score: int,
) -> dict[str, int]:
    if mode == ResponseMode.SPOKEN_ANSWER:
        return {
            "benchmark_gap_coverage": benchmark_score,
            "answer_relevance": response_strength,
            "evidence_examples": max(benchmark_score, response_strength - 5),
            "communication_clarity": communication_score,
            "role_specific_depth": response_strength,
            "audio_professionalism": communication_score,
        }
    if mode == ResponseMode.WRITTEN_ANSWER:
        return {
            "relevance": text_score,
            "structure": response_strength,
            "evidence_specificity": max(benchmark_score, text_score - 5),
            "completeness": response_strength,
            "benchmark_gap_coverage": benchmark_score,
            "clarity": text_score,
        }
    if mode == ResponseMode.CODE_ANSWER:
        return {
            "code_correctness": code_score,
            "reasoning_explanation": response_strength,
            "complexity": max(55, code_score - 5),
            "edge_cases": max(50, code_score - 10),
            "readability_testability": code_score,
            "benchmark_relevance": benchmark_score,
        }
    return {
        "benchmark_gap_coverage": benchmark_score,
        "spoken_quality": communication_score,
        "written_quality": text_score,
        "code_quality": code_score,
    }


def _benchmark_gap_score(result: AgentResult | None) -> int:
    if result is None:
        return 50
    payload = result.payload or {}
    raw_score = payload.get("benchmark_gap_coverage_score", result.score)
    return _normalize_score(raw_score, scale=10 if _as_float(raw_score) <= 10 else 100)


def _communication_score(answer: CandidateAnswer, result: AgentResult | None) -> int:
    payload = result.payload if result is not None else answer.communication_metrics or {}
    raw_score = payload.get("communication_signal_score")
    if raw_score is None:
        raw_score = payload.get("score")
    return _normalize_score(raw_score, scale=10) if raw_score is not None else 65


def _agent_score(result: AgentResult | None, *, default: int) -> int:
    if result is None:
        return default
    return _normalize_score(result.score, scale=10 if (result.score or 0) <= 10 else 100)


def _response_strength(answer: CandidateAnswer) -> int:
    text = "\n".join(
        part
        for part in (answer.transcript, answer.text_answer, answer.code_answer)
        if part
    )
    word_count = len(text.split())
    if word_count >= 120:
        return 82
    if word_count >= 60:
        return 74
    if word_count >= 25:
        return 66
    if word_count > 0:
        return 55
    return 40


def _store_answer_evaluation(
    db: Session,
    *,
    answer_id: str,
    result: FinalEvaluationResult,
) -> AnswerEvaluation:
    row = AnswerEvaluation(
        answer_id=answer_id,
        relevance_score=_pick_score(result.category_scores, ["answer_relevance", "relevance"]),
        role_depth_score=_pick_score(result.category_scores, ["role_specific_depth", "reasoning_explanation"]),
        evidence_score=_pick_score(result.category_scores, ["evidence_examples", "evidence_specificity"]),
        clarity_score=_pick_score(result.category_scores, ["communication_clarity", "clarity"]),
        structure_score=_pick_score(result.category_scores, ["structure", "readability_testability"]),
        jd_alignment_score=_pick_score(result.category_scores, ["benchmark_relevance", "benchmark_gap_coverage"]),
        benchmark_gap_coverage_score=result.category_scores.get("benchmark_gap_coverage"),
        communication_score=_pick_score(result.category_scores, ["communication_clarity", "audio_professionalism", "spoken_quality"]),
        communication_signal_score=_pick_score(result.category_scores, ["communication_clarity", "audio_professionalism", "spoken_quality"]),
        code_quality_score=_pick_score(result.category_scores, ["code_correctness", "code_quality"]),
        written_answer_score=_pick_score(result.category_scores, ["relevance", "written_quality"]),
        visual_signal_score=None,
        overall_score=result.overall_score,
        strengths="\n".join(result.strengths),
        weaknesses="\n".join(result.weaknesses),
        strict_feedback=result.strict_feedback,
        red_flags=[],
        modality_breakdown=result.modality_breakdown,
        improved_answer=json.dumps(
            {
                "improvement_suggestions": result.improvement_suggestions,
                "benchmark_gap_summary": result.benchmark_gap_summary,
                "communication_summary": result.communication_summary,
                "modality_breakdown": result.modality_breakdown,
            },
            ensure_ascii=False,
        ),
    )
    db.add(row)
    return row


def _feedback_lists(
    category_scores: dict[str, int],
    *,
    benchmark_score: int,
    communication_score: int,
) -> tuple[list[str], list[str], list[str]]:
    strengths = []
    weaknesses = []
    improvements = []

    if benchmark_score >= 70:
        strengths.append("Response addresses the benchmark gap with usable evidence.")
    else:
        weaknesses.append("Benchmark gap coverage is not yet strong enough.")
        improvements.append("Tie the answer directly to the benchmark gap with concrete proof.")

    if communication_score >= 70:
        strengths.append("Communication signals are clear enough to support the answer.")
    else:
        weaknesses.append("Communication clarity needs tighter structure and pacing.")
        improvements.append("Use a clearer context-action-impact structure.")

    weakest = min(category_scores, key=category_scores.get)
    if category_scores[weakest] < 65:
        weaknesses.append(f"Weakest scoring area: {weakest.replace('_', ' ')}.")
        improvements.append(f"Improve {weakest.replace('_', ' ')} before relying on this answer.")

    if not strengths:
        strengths.append("Response has enough content to evaluate, but needs sharper evidence.")

    return strengths, weaknesses, improvements


def _strict_feedback(overall: int, mode: ResponseMode, benchmark_score: int) -> str:
    if overall >= 80 and benchmark_score >= 70:
        return f"Strong {mode.value} response. It addresses the benchmark gap and has enough evidence to proceed."
    if overall >= 65:
        return f"Moderate {mode.value} response. It is usable, but benchmark proof needs more specificity."
    return f"Weak {mode.value} response. It does not yet prove the benchmark gap at interview standard."


def _benchmark_summary(result: AgentResult | None) -> str:
    if result is None:
        return "No benchmark-gap agent result was available; score uses conservative defaults."
    payload = result.payload or {}
    return payload.get("gap_specific_feedback") or "Benchmark-gap result was available."


def _communication_summary(answer: CandidateAnswer, result: AgentResult | None) -> str:
    payload = result.payload if result is not None else answer.communication_metrics or {}
    observations = payload.get("structure_observations")
    if observations:
        return "; ".join(str(item) for item in observations)
    if answer.answer_mode == ResponseMode.CODE_ANSWER.value:
        return "Communication summary is limited for code-only responses."
    return "No communication agent result was available; score uses conservative defaults."


def _pick_score(scores: dict[str, int], keys: list[str]) -> int | None:
    for key in keys:
        if key in scores:
            return scores[key]
    return None


def _normalize_score(value, *, scale: int) -> int:
    numeric = _as_float(value)
    if scale == 10:
        numeric *= 10
    return max(0, min(100, round(numeric)))


def _as_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
