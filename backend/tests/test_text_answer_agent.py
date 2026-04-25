from __future__ import annotations

from typing import Any

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion, QuestionCategory, ResponseMode
from app.schemas.agent_results import TextAnswerAnalysisResult
from app.services.text_answer_agent import analyze_text_answer
from app.tasks.analyze_text_answer import store_text_answer_agent_result


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
        question_text="Explain a reliability improvement with ownership and metrics.",
        expected_signal="Specific ownership, baseline metric, measurable result.",
        benchmark_gap_refs=["missing reliability metrics", "weak ownership proof"],
        response_mode=ResponseMode.WRITTEN_ANSWER.value,
        requires_text=True,
    )


def _answer() -> CandidateAnswer:
    return CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.WRITTEN_ANSWER.value,
        text_answer=(
            "First, I owned the payments API reliability work. We measured p95 latency, "
            "then reduced latency by 40% after tracing slow queries and adding monitoring. "
            "Therefore the team had clearer ownership and a measurable result."
        ),
    )


def test_text_answer_agent_mock_mode_returns_typed_scores(monkeypatch):
    monkeypatch.setattr("app.services.text_answer_agent.settings.ai_mock_mode", True)
    monkeypatch.setattr("app.services.text_answer_agent.settings.openai_api_key", "")

    result = analyze_text_answer(question=_question(), answer=_answer())

    assert 0 <= result.relevance_score <= 10
    assert 0 <= result.structure_score <= 10
    assert 0 <= result.specificity_score <= 10
    assert 0 <= result.evidence_score <= 10
    assert 0 <= result.clarity_score <= 10
    assert 0 <= result.completeness_score <= 10
    assert result.strengths
    assert isinstance(result.weaknesses, list)
    assert isinstance(result.improvement_suggestions, list)


def test_text_answer_agent_uses_benchmark_gap_refs_in_feedback(monkeypatch):
    monkeypatch.setattr("app.services.text_answer_agent.settings.ai_mock_mode", True)

    result = analyze_text_answer(question=_question(), answer=_answer())

    assert any("benchmark gap" in item.lower() for item in result.strengths)
    assert not any("personality" in item.lower() for item in result.improvement_suggestions)


def test_text_answer_agent_can_analyze_pseudocode_from_code_answer(monkeypatch):
    monkeypatch.setattr("app.services.text_answer_agent.settings.ai_mock_mode", True)
    answer = CandidateAnswer(
        id="answer-code",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.MIXED_ANSWER.value,
        text_answer="I would first validate the input and then explain trade-offs.",
        code_answer="if latency > target: add_tracing()",
    )

    result = analyze_text_answer(question=_question(), answer=answer)

    assert result.structure_score >= 5
    assert result.clarity_score >= 6


def test_text_answer_agent_requires_written_text(monkeypatch):
    monkeypatch.setattr("app.services.text_answer_agent.settings.ai_mock_mode", True)
    answer = CandidateAnswer(
        id="answer-empty",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.WRITTEN_ANSWER.value,
    )

    try:
        analyze_text_answer(question=_question(), answer=answer)
    except ValueError as exc:
        assert "written text" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_store_text_answer_agent_result_persists_agent_result_row():
    db = FakeDB()
    result = TextAnswerAnalysisResult(
        relevance_score=8,
        structure_score=7,
        specificity_score=6,
        evidence_score=5,
        clarity_score=8,
        completeness_score=7,
        strengths=["Relevant answer"],
        weaknesses=["Needs more metrics"],
        improvement_suggestions=["Add quantified impact"],
    )

    row = store_text_answer_agent_result(db, answer_id="answer-1", result=result)

    assert row in db.added
    assert isinstance(row, AgentResult)
    assert row.answer_id == "answer-1"
    assert row.agent_type == AgentType.TEXT_ANSWER.value
    assert row.status == AgentResultStatus.SUCCEEDED.value
    assert row.score == 7.0
    assert row.payload["evidence_score"] == 5


def test_text_answer_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["analyze_text_answer"] == "app.tasks.analyze_text_answer.run"
