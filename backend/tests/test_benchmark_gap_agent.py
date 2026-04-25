from __future__ import annotations

from typing import Any

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion, QuestionCategory, QuestionSource
from app.schemas.agent_results import BenchmarkGapCoverageResult
from app.services.benchmark_gap_agent import analyze_benchmark_gap_coverage
from app.tasks.analyze_benchmark_gap_coverage import store_benchmark_gap_agent_result


class FakeDB:
    def __init__(self) -> None:
        self.added: list[Any] = []

    def add(self, item: Any) -> None:
        self.added.append(item)


def _question() -> InterviewQuestion:
    return InterviewQuestion(
        id="question-1",
        session_id="session-1",
        question_number=1,
        category=QuestionCategory.BENCHMARK_GAP_VALIDATION.value,
        question_text="Quantify a reliability improvement you owned.",
        expected_signal="Specific ownership, baseline metric, measurable result.",
        source=QuestionSource.BENCHMARK_GAP.value,
        benchmark_gap_refs=["missing reliability metrics", "weak ownership proof"],
    )


def _answer() -> CandidateAnswer:
    return CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        transcript=(
            "I owned the payments API reliability work, showed clear ownership proof, and "
            "reduced p95 latency by 40 percent after tracing and query tuning."
        ),
    )


def test_benchmark_gap_agent_mock_mode_uses_question_gap_refs(monkeypatch):
    monkeypatch.setattr("app.services.benchmark_gap_agent.settings.ai_mock_mode", True)
    monkeypatch.setattr("app.services.benchmark_gap_agent.settings.openai_api_key", "")

    result = analyze_benchmark_gap_coverage(question=_question(), answer=_answer())

    assert 1 <= result.benchmark_gap_coverage_score <= 10
    assert result.evidence_quality in {"weak", "moderate", "strong"}
    assert "missing reliability metrics" in result.covered_gaps
    assert "weak ownership proof" in result.covered_gaps
    assert result.gap_specific_feedback
    assert result.remaining_interview_risk


def test_benchmark_gap_agent_reads_text_and_code_when_no_transcript(monkeypatch):
    monkeypatch.setattr("app.services.benchmark_gap_agent.settings.ai_mock_mode", True)
    answer = CandidateAnswer(
        id="answer-2",
        session_id="session-1",
        question_id="question-1",
        text_answer="I owned the rollout and added reliability metrics.",
        code_answer="# latency metric instrumentation",
    )

    result = analyze_benchmark_gap_coverage(question=_question(), answer=answer)

    assert result.covered_gaps
    assert result.benchmark_gap_coverage_score >= 5


def test_store_benchmark_gap_agent_result_persists_agent_result_row():
    db = FakeDB()
    result = BenchmarkGapCoverageResult(
        benchmark_gap_coverage_score=6,
        covered_gaps=["missing reliability metrics"],
        missed_gaps=["weak ownership proof"],
        evidence_quality="moderate",
        gap_specific_feedback="Some metrics were present, ownership proof needs depth.",
        remaining_interview_risk="Follow up on ownership boundaries.",
    )

    row = store_benchmark_gap_agent_result(db, answer_id="answer-1", result=result)

    assert row in db.added
    assert isinstance(row, AgentResult)
    assert row.answer_id == "answer-1"
    assert row.agent_type == AgentType.BENCHMARK_GAP.value
    assert row.status == AgentResultStatus.SUCCEEDED.value
    assert row.score == 6.0
    assert row.payload["evidence_quality"] == "moderate"


def test_benchmark_gap_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert (
        TASK_REGISTRY["analyze_benchmark_gap_coverage"]
        == "app.tasks.analyze_benchmark_gap_coverage.run"
    )
