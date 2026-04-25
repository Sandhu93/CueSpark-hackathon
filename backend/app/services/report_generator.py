from __future__ import annotations

import json
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.evaluation import AnswerEvaluation
from app.models.report import HiringRecommendation, InterviewReport
from app.models.session import InterviewSession


def generate_multimodal_readiness_report(db: Session, session_id: str) -> InterviewReport:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")

    comparison = _latest_benchmark_comparison(db, session_id)
    answers = list(
        db.execute(select(CandidateAnswer).where(CandidateAnswer.session_id == session_id))
        .scalars()
        .all()
    )
    answer_ids = [answer.id for answer in answers]
    evaluations = _evaluations_for_answers(db, answer_ids)
    agent_results = _agent_results_for_answers(db, answer_ids)

    report = build_multimodal_report(
        session=session,
        comparison=comparison,
        answers=answers,
        evaluations=evaluations,
        agent_results=agent_results,
    )
    db.add(report)
    return report


def build_multimodal_report(
    *,
    session: InterviewSession,
    comparison: BenchmarkComparison | None,
    answers: list[CandidateAnswer],
    evaluations: list[AnswerEvaluation],
    agent_results: list[AgentResult],
) -> InterviewReport:
    readiness_score = _average_score([evaluation.overall_score for evaluation in evaluations])
    benchmark_gap_score = _average_score(
        [evaluation.benchmark_gap_coverage_score for evaluation in evaluations]
    )
    communication_score = _average_score(
        [evaluation.communication_score for evaluation in evaluations]
    )
    answer_feedback = _answer_feedback(answers, evaluations)
    modality_summary = _modality_summary(answers, agent_results, benchmark_gap_score, communication_score)

    return InterviewReport(
        session_id=session.id,
        readiness_score=readiness_score,
        hiring_recommendation=_recommendation(readiness_score).value,
        summary=_summary(readiness_score, benchmark_gap_score),
        benchmark_similarity_score=_first_not_none(
            session.benchmark_similarity_score,
            comparison.benchmark_similarity_score if comparison else None,
        ),
        resume_competitiveness_score=_first_not_none(
            session.resume_competitiveness_score,
            comparison.resume_competitiveness_score if comparison else None,
        ),
        evidence_strength_score=_first_not_none(
            session.evidence_strength_score,
            comparison.evidence_strength_score if comparison else None,
        ),
        skill_gaps=_skill_gaps(comparison),
        benchmark_gaps=_benchmark_gaps(comparison, agent_results),
        interview_risk_areas=list(comparison.interview_risk_areas if comparison else []),
        answer_feedback=answer_feedback,
        benchmark_gap_coverage_summary=_benchmark_gap_summary(benchmark_gap_score, agent_results),
        audio_communication_summary=modality_summary.get("audio_communication_summary"),
        visual_signal_summary=modality_summary.get("visual_signal_summary"),
        written_answer_quality_summary=modality_summary.get("written_answer_quality_summary"),
        code_answer_quality_summary=modality_summary.get("code_answer_quality_summary"),
        multimodal_summary=modality_summary,
        resume_feedback=_resume_feedback(comparison),
        improvement_plan=_improvement_plan(comparison, benchmark_gap_score, communication_score),
    )


def _latest_benchmark_comparison(db: Session, session_id: str) -> BenchmarkComparison | None:
    return (
        db.execute(
            select(BenchmarkComparison)
            .where(BenchmarkComparison.session_id == session_id)
            .order_by(BenchmarkComparison.created_at.desc())
        )
        .scalars()
        .first()
    )


def _evaluations_for_answers(db: Session, answer_ids: list[str]) -> list[AnswerEvaluation]:
    if not answer_ids:
        return []
    return list(
        db.execute(select(AnswerEvaluation).where(AnswerEvaluation.answer_id.in_(answer_ids)))
        .scalars()
        .all()
    )


def _agent_results_for_answers(db: Session, answer_ids: list[str]) -> list[AgentResult]:
    if not answer_ids:
        return []
    return list(
        db.execute(
            select(AgentResult).where(
                AgentResult.answer_id.in_(answer_ids),
                AgentResult.status == AgentResultStatus.SUCCEEDED.value,
            )
        )
        .scalars()
        .all()
    )


def _answer_feedback(
    answers: list[CandidateAnswer],
    evaluations: list[AnswerEvaluation],
) -> list[dict]:
    by_answer_id = {evaluation.answer_id: evaluation for evaluation in evaluations}
    feedback = []
    for index, answer in enumerate(answers, 1):
        evaluation = by_answer_id.get(answer.id)
        feedback.append(
            {
                "answer_id": answer.id,
                "question_id": answer.question_id,
                "answer_number": index,
                "answer_mode": answer.answer_mode,
                "overall_score": evaluation.overall_score if evaluation else None,
                "benchmark_gap_coverage_score": (
                    evaluation.benchmark_gap_coverage_score if evaluation else None
                ),
                "communication_score": evaluation.communication_score if evaluation else None,
                "strict_feedback": evaluation.strict_feedback if evaluation else None,
                "strengths": _split_lines(evaluation.strengths if evaluation else None),
                "weaknesses": _split_lines(evaluation.weaknesses if evaluation else None),
            }
        )
    return feedback


def _modality_summary(
    answers: list[CandidateAnswer],
    agent_results: list[AgentResult],
    benchmark_gap_score: int | None,
    communication_score: int | None,
) -> dict:
    by_type: dict[str, list[AgentResult]] = {}
    for result in agent_results:
        by_type.setdefault(result.agent_type, []).append(result)

    summary = {
        "answer_modes": sorted({answer.answer_mode for answer in answers if answer.answer_mode}),
        "answer_count": len(answers),
        "benchmark_gap_average": benchmark_gap_score,
        "communication_average": communication_score,
    }
    if AgentType.AUDIO.value in by_type:
        summary["audio_communication_summary"] = _summarize_agent_payloads(
            by_type[AgentType.AUDIO.value],
            key="communication_signal_score",
            label="communication signal summary",
        )
    elif communication_score is not None:
        summary["audio_communication_summary"] = (
            f"Communication signal summary: average communication score {communication_score}/100."
        )

    if AgentType.VIDEO_SIGNAL.value in by_type:
        summary["visual_signal_summary"] = _summarize_agent_payloads(
            by_type[AgentType.VIDEO_SIGNAL.value],
            key="visual_signal_score",
            label="visual signal summary",
        )

    if AgentType.TEXT_ANSWER.value in by_type:
        summary["written_answer_quality_summary"] = _summarize_agent_payloads(
            by_type[AgentType.TEXT_ANSWER.value],
            key="score",
            label="written answer quality summary",
        )

    if AgentType.CODE_EVALUATION.value in by_type:
        summary["code_answer_quality_summary"] = _summarize_agent_payloads(
            by_type[AgentType.CODE_EVALUATION.value],
            key="score",
            label="code answer quality summary",
        )

    return summary


def _summarize_agent_payloads(agent_results: list[AgentResult], *, key: str, label: str) -> str:
    scores = [
        _payload_score(result.payload, key, result.score)
        for result in agent_results
    ]
    scores = [score for score in scores if score is not None]
    if scores:
        return f"{label}: average {round(mean(scores))}/100 across {len(scores)} answer(s)."
    return f"{label}: available for {len(agent_results)} answer(s)."


def _payload_score(payload: dict, key: str, fallback: float | None) -> int | None:
    value = payload.get(key, fallback)
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if numeric <= 10:
        numeric *= 10
    return max(0, min(100, round(numeric)))


def _benchmark_gap_summary(
    benchmark_gap_score: int | None,
    agent_results: list[AgentResult],
) -> str:
    benchmark_results = [
        result for result in agent_results if result.agent_type == AgentType.BENCHMARK_GAP.value
    ]
    missed_gaps = []
    covered_gaps = []
    for result in benchmark_results:
        covered_gaps.extend(result.payload.get("covered_gaps", []))
        missed_gaps.extend(result.payload.get("missed_gaps", []))
    if benchmark_gap_score is None:
        return "No benchmark gap coverage evaluation is available yet."
    if missed_gaps:
        return (
            f"Benchmark gap coverage averages {benchmark_gap_score}/100. "
            f"Remaining gaps: {', '.join(sorted(set(str(gap) for gap in missed_gaps)))}."
        )
    if covered_gaps:
        return (
            f"Benchmark gap coverage averages {benchmark_gap_score}/100. "
            "The evaluated answers address the referenced benchmark gaps."
        )
    return f"Benchmark gap coverage averages {benchmark_gap_score}/100."


def _skill_gaps(comparison: BenchmarkComparison | None) -> list:
    if comparison is None:
        return []
    return list(comparison.missing_skills or []) + list(comparison.weak_skills or [])


def _benchmark_gaps(
    comparison: BenchmarkComparison | None,
    agent_results: list[AgentResult],
) -> list:
    gaps = []
    if comparison is not None:
        gaps.extend(comparison.missing_metrics or [])
        gaps.extend(comparison.weak_ownership_signals or [])
        gaps.extend(comparison.question_targets or [])
    for result in agent_results:
        if result.agent_type == AgentType.BENCHMARK_GAP.value:
            gaps.extend(result.payload.get("missed_gaps", []))
    return sorted(set(str(gap) for gap in gaps if str(gap).strip()))


def _resume_feedback(comparison: BenchmarkComparison | None) -> str:
    fixes = list(comparison.recommended_resume_fixes if comparison else [])
    if not fixes:
        return "Add concrete evidence, measurable outcomes, and ownership scope to the resume."
    return "\n".join(str(fix) for fix in fixes)


def _improvement_plan(
    comparison: BenchmarkComparison | None,
    benchmark_gap_score: int | None,
    communication_score: int | None,
) -> str:
    steps = []
    if benchmark_gap_score is None or benchmark_gap_score < 70:
        steps.append("Prepare STAR stories that directly prove the highest-priority benchmark gaps.")
    if communication_score is not None and communication_score < 70:
        steps.append("Practice concise context-action-impact delivery for spoken answers.")
    if comparison is not None and comparison.missing_metrics:
        steps.append("Add metrics such as latency, error rate, throughput, cost, revenue, or user impact.")
    if not steps:
        steps.append("Maintain benchmark-specific practice and rehearse concise evidence-backed answers.")
    return "\n".join(steps)


def _summary(readiness_score: int | None, benchmark_gap_score: int | None) -> str:
    if readiness_score is None:
        return "Readiness report generated with limited evaluation data."
    if readiness_score >= 80 and (benchmark_gap_score or 0) >= 70:
        return "Strong readiness signal. Answers are benchmark-aware and supported by useful evidence."
    if readiness_score >= 65:
        return "Moderate readiness signal. The candidate needs stronger benchmark-gap proof before applying."
    return "Low readiness signal. The candidate should improve evidence depth and benchmark-gap coverage."


def _recommendation(readiness_score: int | None) -> HiringRecommendation:
    if readiness_score is None:
        return HiringRecommendation.MAYBE
    if readiness_score >= 85:
        return HiringRecommendation.STRONG_YES
    if readiness_score >= 75:
        return HiringRecommendation.YES
    if readiness_score >= 55:
        return HiringRecommendation.MAYBE
    return HiringRecommendation.NO


def _average_score(values: list[int | None]) -> int | None:
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return round(mean(cleaned))


def _first_not_none(*values: int | None) -> int | None:
    for value in values:
        if value is not None:
            return value
    return None


def _split_lines(value: str | None) -> list[str]:
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]
