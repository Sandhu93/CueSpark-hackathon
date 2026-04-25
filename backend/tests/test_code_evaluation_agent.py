from __future__ import annotations

from typing import Any

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion, QuestionCategory, ResponseMode
from app.schemas.agent_results import CodeEvaluationResult
from app.services.code_evaluation_agent import analyze_code_answer
from app.tasks.analyze_code_answer import store_code_evaluation_agent_result


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
        category=QuestionCategory.TECHNICAL.value,
        question_text="Implement a function that returns the first duplicate value.",
        expected_signal="Correctness, edge cases, complexity, readable implementation.",
        benchmark_gap_refs=["algorithmic edge cases", "complexity explanation"],
        response_mode=ResponseMode.CODE_ANSWER.value,
        requires_code=True,
    )


def _answer() -> CandidateAnswer:
    return CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.CODE_ANSWER.value,
        code_language="python",
        code_answer=(
            "def first_duplicate(values):\n"
            "    seen = set()\n"
            "    for value in values:\n"
            "        if value in seen:\n"
            "            return value\n"
            "        seen.add(value)\n"
            "    return None\n"
            "\n"
            "assert first_duplicate([1, 2, 1]) == 1\n"
        ),
        text_answer="I use a set to track seen values, so the time complexity is linear.",
    )


def test_code_evaluation_agent_mock_mode_returns_static_review(monkeypatch):
    monkeypatch.setattr("app.services.code_evaluation_agent.settings.ai_mock_mode", True)
    monkeypatch.setattr("app.services.code_evaluation_agent.settings.openai_api_key", "")

    result = analyze_code_answer(question=_question(), answer=_answer())

    assert 0 <= result.correctness_score <= 10
    assert 0 <= result.edge_case_score <= 10
    assert 0 <= result.complexity_score <= 10
    assert 0 <= result.readability_score <= 10
    assert 0 <= result.testability_score <= 10
    assert 0 <= result.explanation_score <= 10
    assert result.strengths
    assert result.complexity_analysis.startswith("Static review only")


def test_code_evaluation_agent_does_not_execute_candidate_code(monkeypatch):
    monkeypatch.setattr("app.services.code_evaluation_agent.settings.ai_mock_mode", True)
    answer = CandidateAnswer(
        id="answer-danger",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.CODE_ANSWER.value,
        code_language="python",
        code_answer="raise RuntimeError('would execute if unsafe')",
    )

    result = analyze_code_answer(question=_question(), answer=answer)

    assert result.correctness_score <= 7
    assert "Static review only" in result.complexity_analysis


def test_code_evaluation_agent_requires_code(monkeypatch):
    monkeypatch.setattr("app.services.code_evaluation_agent.settings.ai_mock_mode", True)
    answer = CandidateAnswer(
        id="answer-empty",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.CODE_ANSWER.value,
    )

    try:
        analyze_code_answer(question=_question(), answer=answer)
    except ValueError as exc:
        assert "no code" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_store_code_evaluation_agent_result_persists_agent_result_row():
    db = FakeDB()
    result = CodeEvaluationResult(
        correctness_score=7,
        edge_case_score=6,
        complexity_score=8,
        readability_score=7,
        testability_score=6,
        explanation_score=7,
        strengths=["Uses a set for lookup"],
        weaknesses=["Needs more edge cases"],
        suggested_improvements=["Add empty input tests"],
        complexity_analysis="Static review only: appears O(n).",
    )

    row = store_code_evaluation_agent_result(db, answer_id="answer-1", result=result)

    assert row in db.added
    assert isinstance(row, AgentResult)
    assert row.answer_id == "answer-1"
    assert row.agent_type == AgentType.CODE_EVALUATION.value
    assert row.status == AgentResultStatus.SUCCEEDED.value
    assert row.score == 7.0
    assert row.payload["correctness_score"] == 7


def test_code_evaluation_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["analyze_code_answer"] == "app.tasks.analyze_code_answer.run"
