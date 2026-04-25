from __future__ import annotations

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.evaluation import AnswerEvaluation
from app.models.report import HiringRecommendation, InterviewReport
from app.models.session import InterviewSession
from app.services.report_generator import build_multimodal_report


def _session() -> InterviewSession:
    return InterviewSession(
        id="session-1",
        job_description_text="Senior backend role.",
        benchmark_similarity_score=54,
        resume_competitiveness_score=48,
        evidence_strength_score=39,
    )


def _comparison() -> BenchmarkComparison:
    return BenchmarkComparison(
        id="comparison-1",
        session_id="session-1",
        role_key="backend_developer",
        benchmark_similarity_score=55,
        resume_competitiveness_score=50,
        evidence_strength_score=42,
        missing_skills=["observability"],
        weak_skills=["architecture trade-offs"],
        missing_metrics=["latency improvement metric"],
        weak_ownership_signals=["post-launch ownership"],
        interview_risk_areas=["may not quantify backend reliability impact"],
        recommended_resume_fixes=["Add p95 latency and error-rate improvement metrics."],
        question_targets=["validate ownership proof"],
    )


def _answers() -> list[CandidateAnswer]:
    return [
        CandidateAnswer(
            id="answer-1",
            session_id="session-1",
            question_id="question-1",
            answer_mode="spoken_answer",
            transcript="I owned reliability work and reduced latency.",
        ),
        CandidateAnswer(
            id="answer-2",
            session_id="session-1",
            question_id="question-2",
            answer_mode="code_answer",
            code_answer="def solve(): return True",
        ),
    ]


def _evaluations() -> list[AnswerEvaluation]:
    return [
        AnswerEvaluation(
            id="evaluation-1",
            answer_id="answer-1",
            overall_score=72,
            benchmark_gap_coverage_score=70,
            communication_score=80,
            strict_feedback="Usable spoken response, but needs deeper ownership detail.",
            strengths="Clear reliability example",
            weaknesses="Ownership boundaries need detail",
        ),
        AnswerEvaluation(
            id="evaluation-2",
            answer_id="answer-2",
            overall_score=62,
            benchmark_gap_coverage_score=55,
            communication_score=None,
            strict_feedback="Code response needs stronger explanation.",
            strengths="Readable structure",
            weaknesses="Missing edge cases",
        ),
    ]


def _agent_results() -> list[AgentResult]:
    return [
        AgentResult(
            answer_id="answer-1",
            agent_type=AgentType.BENCHMARK_GAP.value,
            status=AgentResultStatus.SUCCEEDED.value,
            payload={
                "covered_gaps": ["missing reliability metrics"],
                "missed_gaps": ["weak ownership proof"],
                "gap_specific_feedback": "Some metrics were present, ownership proof needs depth.",
            },
        ),
        AgentResult(
            answer_id="answer-1",
            agent_type=AgentType.AUDIO.value,
            status=AgentResultStatus.SUCCEEDED.value,
            payload={"communication_signal_score": 8},
        ),
        AgentResult(
            answer_id="answer-2",
            agent_type=AgentType.CODE_EVALUATION.value,
            status=AgentResultStatus.SUCCEEDED.value,
            score=6,
            payload={"score": 6},
        ),
    ]


def test_build_multimodal_report_aggregates_scores_and_benchmark_gaps():
    report = build_multimodal_report(
        session=_session(),
        comparison=_comparison(),
        answers=_answers(),
        evaluations=_evaluations(),
        agent_results=_agent_results(),
    )

    assert isinstance(report, InterviewReport)
    assert report.readiness_score == 67
    assert report.hiring_recommendation == HiringRecommendation.MAYBE.value
    assert report.benchmark_similarity_score == 54
    assert "observability" in report.skill_gaps
    assert "weak ownership proof" in report.benchmark_gaps
    assert report.benchmark_gap_coverage_summary
    assert "weak ownership proof" in report.benchmark_gap_coverage_summary
    assert len(report.answer_feedback) == 2


def test_build_multimodal_report_includes_only_available_modality_summaries():
    report = build_multimodal_report(
        session=_session(),
        comparison=_comparison(),
        answers=_answers(),
        evaluations=_evaluations(),
        agent_results=_agent_results(),
    )

    assert report.audio_communication_summary is not None
    assert report.code_answer_quality_summary is not None
    assert report.visual_signal_summary is None
    assert report.written_answer_quality_summary is None
    assert report.multimodal_summary["answer_count"] == 2
    assert sorted(report.multimodal_summary["answer_modes"]) == ["code_answer", "spoken_answer"]


def test_build_multimodal_report_remains_useful_with_only_audio_data():
    answers = [_answers()[0]]
    evaluations = [_evaluations()[0]]
    agent_results = [result for result in _agent_results() if result.agent_type == AgentType.AUDIO.value]

    report = build_multimodal_report(
        session=_session(),
        comparison=None,
        answers=answers,
        evaluations=evaluations,
        agent_results=agent_results,
    )

    assert report.readiness_score == 72
    assert report.skill_gaps == []
    assert report.benchmark_gaps == []
    assert report.audio_communication_summary is not None
    assert report.benchmark_gap_coverage_summary == (
        "Benchmark gap coverage averages 70/100."
    )
    assert "selection guarantee" not in (report.summary or "").lower()


def test_generate_report_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["generate_report"] == "app.tasks.generate_report.run"
