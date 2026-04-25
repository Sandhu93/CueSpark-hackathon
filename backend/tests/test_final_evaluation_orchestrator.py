from __future__ import annotations

from typing import Any

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.evaluation import AnswerEvaluation
from app.models.question import ResponseMode
from app.services.final_evaluation_orchestrator import (
    evaluate_answer,
    orchestrate_final_evaluation,
)


class FakeResult:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def scalars(self) -> "FakeResult":
        return self

    def all(self) -> list[Any]:
        return self.rows


class FakeDB:
    def __init__(self, answer: CandidateAnswer, agent_results: list[AgentResult]) -> None:
        self.answer = answer
        self.agent_results = agent_results
        self.added: list[Any] = []

    def get(self, model_cls: type, pk: str) -> Any:
        if model_cls is CandidateAnswer and pk == self.answer.id:
            return self.answer
        return None

    def execute(self, stmt: Any) -> FakeResult:
        return FakeResult(self.agent_results)

    def add(self, item: Any) -> None:
        self.added.append(item)


def _answer(mode: ResponseMode) -> CandidateAnswer:
    return CandidateAnswer(
        id=f"answer-{mode.value}",
        session_id="session-1",
        question_id="question-1",
        answer_mode=mode.value,
        transcript="I owned the API reliability work and reduced latency with measurable impact.",
        text_answer="Written evidence with metrics and ownership scope.",
        code_answer="def solve(): return True",
        communication_metrics={"communication_signal_score": 7},
    )


def _benchmark_result(score: int = 7) -> AgentResult:
    return AgentResult(
        answer_id="answer-1",
        agent_type=AgentType.BENCHMARK_GAP.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=float(score),
        payload={
            "benchmark_gap_coverage_score": score,
            "gap_specific_feedback": "The answer partially proves the benchmark gap.",
        },
    )


def _audio_result(score: int = 8) -> AgentResult:
    return AgentResult(
        answer_id="answer-1",
        agent_type=AgentType.AUDIO.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=float(score),
        payload={
            "communication_signal_score": score,
            "structure_observations": ["Mentions ownership", "Mentions impact"],
        },
    )


def test_spoken_answer_weights_benchmark_and_communication_results():
    result = orchestrate_final_evaluation(
        answer=_answer(ResponseMode.SPOKEN_ANSWER),
        agent_results=[_benchmark_result(7), _audio_result(8)],
    )

    assert result.category_scores["benchmark_gap_coverage"] == 70
    assert result.category_scores["communication_clarity"] == 80
    assert result.modality_breakdown["answer_mode"] == "spoken_answer"
    assert result.overall_score >= 65


def test_written_answer_uses_written_scoring_shape():
    result = orchestrate_final_evaluation(
        answer=_answer(ResponseMode.WRITTEN_ANSWER),
        agent_results=[_benchmark_result(6)],
    )

    assert set(result.category_scores) == {
        "relevance",
        "structure",
        "evidence_specificity",
        "completeness",
        "benchmark_gap_coverage",
        "clarity",
    }
    assert result.modality_breakdown["answer_mode"] == "written_answer"


def test_code_answer_uses_code_scoring_shape():
    result = orchestrate_final_evaluation(
        answer=_answer(ResponseMode.CODE_ANSWER),
        agent_results=[_benchmark_result(5)],
    )

    assert "code_correctness" in result.category_scores
    assert "edge_cases" in result.category_scores
    assert result.modality_breakdown["answer_mode"] == "code_answer"


def test_missing_optional_agent_results_do_not_crash_orchestration():
    result = orchestrate_final_evaluation(
        answer=_answer(ResponseMode.MIXED_ANSWER),
        agent_results=[],
    )

    assert result.overall_score > 0
    assert result.benchmark_gap_summary.startswith("No benchmark-gap agent result")
    assert result.modality_breakdown["answer_mode"] == "mixed_answer"


def test_evaluate_answer_stores_answer_evaluation_row():
    answer = _answer(ResponseMode.SPOKEN_ANSWER)
    db = FakeDB(answer, [_benchmark_result(7), _audio_result(8)])

    result, row = evaluate_answer(db, answer.id)

    assert row in db.added
    assert isinstance(row, AnswerEvaluation)
    assert row.answer_id == answer.id
    assert row.overall_score == result.overall_score
    assert row.benchmark_gap_coverage_score == 70
    assert row.communication_score == 80
    assert row.strict_feedback == result.strict_feedback
    assert "benchmark_gap_summary" in row.improved_answer


def test_evaluate_answer_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["evaluate_answer"] == "app.tasks.evaluate_answer.run"
